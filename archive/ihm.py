from tkinter.filedialog import *
from tkinter.messagebox import showerror
import queue
from threading import Thread
from time import time
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pattern

#identifier le format des coordonnées
def identifier(msg):
    liste=['0','1','2','3','4','5','6','7','8','9']
    i=0
    for i in range(len(msg)):
        if msg[i] in liste:
            return True
        else:
            print("erreur de formatage de coordonnées")
            return False

def parseGPS(trame):
    data = trame.split(',')
    if len(data) != 8:
        return [0]

    if data[3] == 'S':
        data[3] = -1
    else:
        data[3] = 1
    if data[7] == 'W':
        data[7] = -1
    else:
        data[7] = 1
    return [float(d) for d in data]


class IHM():

    def onclick_map(self, event):
        if event.xdata != None:
            lon, lat = self.map(event.xdata, event.ydata, inverse = True)
            x, y = self.map(lon, lat)
            self.map.scatter(x,y,150,marker='*',color='g')
            way = pattern.ratissage_sc([x, y], 50,5,5,0)
            patx=[]
            paty=[]
            way = way.transpose()
            self.map.plot(way[0], way[1])
            self.canvas.draw()
        else:
            showerror("Error", "Veuillez selectionner un point dans la carte")


    #recevoir les coordonnées
    def update(self):
        try:
            temp = self.queue.get_nowait()
            if(temp.startswith("GPS")):
                self.zone_reception.delete("1.0", END)
                self.zone_reception.insert(INSERT, temp[3:])
                coord = parseGPS(temp[3:])
                if coord[0] != 0:
                    lat = coord[3]*(coord[0]+coord[1]/60.0+coord[2]/3600.0)
                    lon = coord[7]*(coord[4]+coord[5]/60.0+coord[6]/3600.0)
                    x, y = self.map(lon, lat) # (-4.47, 48.418)
                    if hasattr(self, 'drone_dot'):
                        self.drone_dot.remove()
                    self.drone_dot = self.map.scatter(x,y,150,marker='o',color='r')
                    self.canvas.draw()
        except queue.Empty:
            # It's ok if there's no data to read.
            # We'll just check again later.
            pass
        self.fenetre.after(2000, self.update)

    #envoyer des coordonnées
    def envoyer_pos(self):
        deg_lat=self.msg_deg_lat.get()
        min_lat=self.msg_min_lat.get()
        sec_lat=self.msg_sec_lat.get()
        deg_long=self.msg_deg_long.get()
        min_long=self.msg_min_long.get()
        sec_long=self.msg_sec_long.get()
        if (identifier(deg_lat) & identifier(min_lat) & identifier(sec_lat)) and\
            (identifier(deg_long) & identifier(min_long) & identifier(sec_long)):
            wp = str(deg_lat)+','+str(min_lat) + ',' + str(sec_lat)+','+str(self.value_lat.get())+ ','+ str(deg_long)+','+str(min_long) + ',' + str(sec_long)+','+str(self.value_long.get())
            self.base.sender.send_text("ADDWAY"+wp)

        '''zone_deg_lat.delete(0,END)
        zone_sec_lat.delete(0,END)
        zone_min_lat.delete(0,END)
        zone_deg_long.delete(0,END)
        zone_sec_long.delete(0,END)
        zone_min_long.delete(0,END)
        zone_reception.delete("1.0", END)'''

    def __init__(self, base, queue):
        self.base = base
        self.queue = queue

        #Gestion de la fenetre
        self.fenetre = Tk() #création de la fenêtre, nom au choix
        self.fenetre.title("Centre de contrôle SAUVMER") #nom de la fenetre
        #self.fenetre['bg']='grey'
        FWidth=self.fenetre.winfo_screenwidth()
        FHeight=self.fenetre.winfo_screenheight()
        label = Label(self.fenetre, text="Bienvenue au centre de contrôle SAUVMER", )
        label['fg']='blue' #création du texte de couleur bleue
        label['bg']='white' #couleur fond de texte
        label.pack(fill=X)#insère le texte dans la fenetre
        
        #gestion des onglets
        nb = ttk.Notebook(self.fenetre)
        #premier onglet
        onglet1 = ttk.Frame(nb)
        nb.add(onglet1, text='Positionnement du drone')
        #deuxieme onglet
        onglet2 = ttk.Frame(nb)
        nb.add(onglet2, text='Données de navigation')
        #troisieme onglet
        onglet3 = ttk.Frame(nb)
        nb.add(onglet3, text='Flux vidéo')
        #quatrieme onglet
        onglet4 = ttk.Frame(nb)
        nb.add(onglet4, text='Information sur la batterie')
        nb.pack(fill=X)


        #case envoyer & recevoir data coordonnees
        l_pos = LabelFrame(onglet1, text="Positionnement du drone", padx=20, pady=20)
        l_pos.pack(fill="both", expand="yes")

        #case afficher carte
        l_map = LabelFrame(onglet1, text="Carte", padx=20, pady=20)
        l_map.pack(fill="both", expand="yes")

        # Bouton actualisation des coordonnees
        #bouton_coord= Button (l_pos, text="Obtenir les coordonnées", command=self.afficher_pos)
        #bouton_coord.grid(row=0,column=0)

        #zone_reception = Canvas(l_pos,width=200, height= 25,background='white') #Définit les dimensions du canevas
        self.zone_reception = Text(l_pos,width=25, height= 1,background='white')
        self.zone_reception.grid(row= 0, column =1) #Affiche le canevas

        # label latitude
        label_lat = Label(l_pos, text="Latitude")
        label_lat.grid(row= 1, column =0)

        # label longitude
        label_long = Label(l_pos, text="Longitude")
        label_long.grid(row= 2, column =0)

        #bouton radio Nord et Sud
        self.value_lat = StringVar()
        bouton1 = Radiobutton(l_pos, text="N", variable=self.value_lat, value='N')
        bouton2 = Radiobutton(l_pos, text="S", variable=self.value_lat, value='S')
        bouton1.grid(row= 1, column =7)
        bouton2.grid(row= 1, column =8)

        #bouton radio Est et Ouest
        self.value_long = StringVar()
        bouton3 = Radiobutton(l_pos, text="O", variable=self.value_long, value='O')
        bouton4 = Radiobutton(l_pos, text="E", variable=self.value_long, value='E')
        bouton3.grid(row= 2, column =7)
        bouton4.grid(row= 2, column =8)

        #zones degré
        self.msg_deg_lat = StringVar()
        zone_deg_lat = Entry(l_pos,background='white',textvariable=self.msg_deg_lat)
        zone_deg_lat.grid(row = 1, column = 1)
        self.msg_deg_long = StringVar()
        zone_deg_long = Entry(l_pos,background='white',textvariable=self.msg_deg_long)
        zone_deg_long.grid(row = 2, column = 1)

        #label degré
        label_deg_lat=Label(l_pos, text='°')
        label_deg_lat.grid(row=1,column = 2)
        label_deg_long=Label(l_pos, text='°')
        label_deg_long.grid(row=2,column = 2)

        #zones minutes
        self.msg_min_lat = StringVar()
        zone_min_lat = Entry(l_pos,background='white',textvariable=self.msg_min_lat)
        zone_min_lat.grid(row = 1, column = 3)
        self.msg_min_long = StringVar()
        zone_min_long = Entry(l_pos,background='white',textvariable=self.msg_min_long)
        zone_min_long.grid(row = 2, column = 3)

        #label minutes
        label_min_lat=Label(l_pos, text="'")
        label_min_lat.grid(row=1,column = 4)
        label_min_long=Label(l_pos, text="'")
        label_min_long.grid(row=2,column = 4)

        #zones secondes
        self.msg_sec_lat = StringVar()
        zone_sec_lat = Entry(l_pos,background='white',textvariable=self.msg_sec_lat)
        zone_sec_lat.grid(row = 1, column = 5)
        self.msg_sec_long = StringVar()
        zone_sec_long = Entry(l_pos,background='white',textvariable=self.msg_sec_long)
        zone_sec_long.grid(row = 2, column = 5)

        #label secondes
        label_sec_lat=Label(l_pos, text='\"')
        label_sec_lat.grid(row=1,column = 6)
        label_sec_long=Label(l_pos, text='\"')
        label_sec_long.grid(row=2,column = 6)

        #bouton envoie coordonnées
        bouton_envoyer = Button(l_pos, text= "Envoyer les coordonnées", command = self.envoyer_pos)
        bouton_envoyer.grid(row=1, column=9)

        #Affichage de la carte
        fig = matplotlib.pyplot.figure(figsize=(12, 6))

        self.map = Basemap(llcrnrlon=-4.476,llcrnrlat=48.417,urcrnrlon=-4.469,urcrnrlat=48.42, epsg=2154)

        self.map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

        self.map.drawcountries()
        self.map.drawcoastlines(linewidth=.5)

        self.canvas = FigureCanvasTkAgg(fig, master=l_map)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=X, expand=1)
        self.canvas.mpl_connect('button_press_event', self.onclick_map)


#gestion de la batterie
        #Frame de la batterie
        l_bat = Label(onglet4)
        l_bat.pack(fill="both", expand = "yes")
        #Voltage
        label_volt = Label(l_bat, text="Voltage battery")
        label_volt.grid(row= 0, column =0)
        zone_reception_volt = Text(l_bat,width=25, height= 1,background='white')
        zone_reception_volt.grid(row= 0, column =1) 
        #Etat
        label_cur = Label(l_bat, text="Current battery")
        label_cur.grid(row= 1, column =0)
        zone_reception_cur = Text(l_bat,width=25, height= 1,background='white')
        zone_reception_cur.grid(row= 1, column =1)    
        #Etat
        label_rem = Label(l_bat, text="battery remaining")
        label_rem.grid(row= 2, column =0)
        zone_reception_rem = Text(l_bat,width=25, height= 1,background='white')
        zone_reception_rem.grid(row= 2, column =1) 
    
#gestion de la navigation
        #Frame de la vitesse (tangage, roulis, lacet)    
        l_vit = LabelFrame(onglet2, text="Vitesse")
        l_vit.pack(fill="both", expand="yes")
        # label roulis
        label_roulis = Label(l_vit, text="Roulis")
        label_roulis.grid(row= 0, column =0)
        zone_reception_roulis = Text(l_vit,width=25, height= 1,background='white')
        zone_reception_roulis.grid(row= 0, column =1) 
        #label tangage
        label_tangage = Label(l_vit, text="Tangage")
        label_tangage.grid(row= 1, column =0)
        zone_reception_tangage = Text(l_vit,width=25, height= 1,background='white')
        zone_reception_tangage.grid(row= 1, column =1)    
        #label lacet
        label_lacet= Label(l_vit, text="Lacet")
        label_lacet.grid(row= 2, column =0)
        zone_reception_lacet = Text(l_vit,width=25, height= 1,background='white')
        zone_reception_lacet.grid(row= 2, column =1) 
    
        #Frame de l'accélération    
        l_acc = LabelFrame(onglet2, text = "Accélération")
        l_acc.pack(fill="both", expand = "yes")
        # label roulis
        label_x = Label(l_acc, text="X")
        label_x.grid(row= 0, column =0)
        zone_reception_x = Text(l_acc,width=25, height= 1,background='white')
        zone_reception_x.grid(row= 0, column =1) 
        #label tangage
        label_y = Label(l_acc, text="Y")
        label_y.grid(row= 1, column =0)
        zone_reception_y = Text(l_acc,width=25, height= 1,background='white')
        zone_reception_y.grid(row= 1, column =1)    
        #label lacet
        label_z= Label(l_acc, text="Z")
        label_z.grid(row= 2, column =0)
        zone_reception_z= Text(l_acc,width=25, height= 1,background='white')
        zone_reception_z.grid(row= 2, column =1) 
    
        #Frame rotation
        l_rot= LabelFrame(onglet2, text = "Rotation")
        l_rot.pack(fill="both", expand = "yes")
        zone_reception_rot= Text(l_rot,width=25, height= 1,background='white')
        zone_reception_rot.grid(row= 2, column =1) 
        
        #Bouton fermeture de la fenetre
        bouton=Button(self.fenetre, text="Fermer", command=self.quit) #Bouton qui détruit la fenêtre
        bouton.pack(side =BOTTOM, padx =1, pady = 1) #insère le bouton dans la boucle

        self.update()

    def quit(self):
        self.fenetre.quit()
        self.fenetre.destroy()