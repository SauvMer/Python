from tkinter.filedialog import *
from tkinter.messagebox import showerror
import queue
from threading import Thread
from time import time
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pattern
import cv2
from PIL import Image, ImageTk
import numpy

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
    data = trame.split(';')
    return [float(data[0]), float(data[1])]

class IHM():

    def __init__(self, rece_queue, send_queue, video_queue):
        self.rece_queue = rece_queue
        self.send_queue = send_queue
        self.video_queue = video_queue

        #Gestion de la fenetre
        self.fenetre = Tk()
        self.fenetre.title("Centre de contrôle SAUVMER")

        #Titre
        label = Label(self.fenetre, text="Bienvenue au centre de contrôle SAUVMER", )
        label['fg']='blue'
        label['bg']='white'
        label.pack(fill=X)
        
        #region GESTION_ONGLET
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
        '''onglet4 = ttk.Frame(nb)
        nb.add(onglet4, text='Information sur la batterie')'''
        nb.pack(fill=X)
        #endregion

        #case envoyer & recevoir data coordonnees
        l_pos = LabelFrame(onglet1, text="Positionnement du drone", padx=20, pady=20)
        l_pos.pack(fill=X, expand="yes")

        l_mis = LabelFrame(onglet1, text="Mission du drone", padx=20, pady=20)
        l_mis.pack(fill=X, expand="yes")

        #case afficher carte
        l_map = LabelFrame(onglet1, text="Carte", padx=20, pady=20)
        l_map.pack(fill=X, expand="yes")

        #zone_reception = Canvas(l_pos,width=200, height= 25,background='white') #Définit les dimensions du canevas
        self.zone_reception = Text(l_pos,width=25, height= 1,background='white')
        self.zone_reception.grid(row= 0, column =0) #Affiche le canevas

        print("Initiailsé")

        #region SEND_COORDONNEE

        '''
        # label latitude/longitude
        label_lat = Label(l_pos, text="Latitude")
        label_lat.grid(row= 1, column =0)
        label_long = Label(l_pos, text="Longitude")
        label_long.grid(row= 2, column =0)

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

        #bouton envoie coordonnées
        bouton_envoyer = Button(l_pos, text= "Envoyer les coordonnées", command = self.envoyer_pos)
        bouton_envoyer.grid(row=1, column=9)
        '''

        self.var = IntVar()
        R1 = Radiobutton(l_mis, text="waypoint", variable=self.var, value=1)
        R1.grid(row=0, column=3, sticky=W)

        R2 = Radiobutton(l_mis, text="spirale carrée", variable=self.var, value=2)
        R2.grid(row=1, column=3, sticky=W)

        R3 = Radiobutton(l_mis, text="lacet", variable=self.var, value=3)
        R3.grid(row=2, column=3, sticky=W)

        launch_button=Button(l_mis, text="Launch mission", command=self.launch, height = 2, width = 20, padx=20)
        launch_button.grid(row=0, column=4, sticky=W)

        clear_button=Button(l_mis, text="Clear mission", command=self.clear_waypoint, height = 2, width = 20, padx=20)
        clear_button.grid(row=1, column=4)

        takeoff_button=Button(l_mis, text="Take off!", command=self.takeoff, height = 2, width = 20, padx=20)
        takeoff_button.grid(row=0, column=5)

        land_button=Button(l_mis, text="Land", command=self.land, height = 2, width = 20, padx=20)
        land_button.grid(row=1, column=5)

        #endregion
        print("Initiailsé")
        #region AFFICHER_CARTE
        fig = plt.figure(figsize=(12, 6))

        self.map = Basemap(llcrnrlon=-4.476,llcrnrlat=48.417, urcrnrlon=-4.469, urcrnrlat=48.42, epsg=2154)
        try:
            self.map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)
            print("Carte chargé online")
        except:
            im = plt.imread('ensta.png')
            self.map.imshow(im)
            print("Carte chargé offline")
        self.mapplot = None

        #self.map.drawcountries()
        #self.map.drawcoastlines(linewidth=.5)

        self.canvas = FigureCanvasTkAgg(fig, master=l_map)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=X, expand=1)
        self.canvas.mpl_connect('button_press_event', self.onclick_map)

        

        #bouton_waypoint = Button(self.canvas, text= "Envoyer les waypoint", command = self.envoyer_way)
        #endregion

        #region BATTERIE
        '''#Frame de la batterie
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
        zone_reception_rem.grid(row= 2, column =1) '''
        #endregion

        #region NAVIGATION
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
        #endregion

        #region VIDEO
        #Graphics window
        imageFrame = tk.Frame(onglet3) #, width=600, height=500
        imageFrame.grid(row=0, column=0, padx=10, pady=2)
        self.image = tk.Label(imageFrame)
        self.image.grid(row=0, column=0)

        #endregion

        print("Initiailsé")

        #region FERMETURE FENETRE
        bouton=Button(self.fenetre, text="Fermer", command=self.quit) #Bouton qui détruit la fenêtre
        bouton.pack(side =BOTTOM, padx =1, pady = 1) #insère le bouton dans la boucle

        #endregion

        self.waypoint = []
        
        print("Initiailsé")

        self.update()

    def onclick_map(self, event):
        if event.xdata != None:
            lon, lat = self.map(event.xdata, event.ydata, inverse = True)
            x, y = self.map(lon, lat)

            if self.mapplot is None:
                self.mapplot, = self.map.plot(x,y,linestyle='-', marker='*', color='k')

            if self.var.get() == 1:
                self.mapplot.set_xdata(numpy.append(self.mapplot.get_xdata(), x))
                self.mapplot.set_ydata(numpy.append(self.mapplot.get_ydata(), y))
                self.waypoint.append((lon, lat))
            elif self.var.get() == 2:
                way = pattern.ratissage_sc([x, y], 50,5,5,0)
                way = way.transpose()
                #self.map.plot(way[0], way[1])
                for k in range(0, len(way[0])):
                    self.mapplot.set_xdata(numpy.append(self.mapplot.get_xdata(), way[0,k]))
                    self.mapplot.set_ydata(numpy.append(self.mapplot.get_ydata(), way[1,k]))
                    self.waypoint.append(self.map(way[0,k],way[1,k], inverse=True))
            elif self.var.get() == 3:
                way = pattern.balai([x, y], [x+30, y+30],10,0)
                way = way.transpose()
                #self.map.plot(way[0], way[1])
                for k in range(0, len(way[0])):
                    self.mapplot.set_xdata(numpy.append(self.mapplot.get_xdata(), way[0,k]))
                    self.mapplot.set_ydata(numpy.append(self.mapplot.get_ydata(), way[1,k]))
                    self.waypoint.append(self.map(way[0,k],way[1,k], inverse=True))

            self.canvas.draw()
            print(self.waypoint)
        else:
            showerror("Error", "Veuillez selectionner un point dans la carte")

    def update(self):
        try:
            temp = self.rece_queue.get_nowait()

            if(temp.startswith("GPS")):
                self.zone_reception.delete("1.0", END)
                self.zone_reception.insert(INSERT, temp[3:])
                coord = parseGPS(temp[3:])
                if coord[0] != 0:
                    lat = coord[0]
                    lon = coord[1]
                    x, y = self.map(lon, lat) # (-4.47, 48.418)
                    if hasattr(self, 'drone_dot'):
                        self.drone_dot.remove()
                    self.drone_dot = self.map.scatter(x,y,70,marker='o',color='r')
                    self.canvas.draw()
            elif(temp.startswith("DETECT")):
                print("Victim detected")
                coord = parseGPS(temp[6:])
                if coord[0] != 0:
                    lat = coord[0]
                    lon = coord[1]
                    x, y = self.map(lon, lat) # (-4.47, 48.418)
                    self.map.scatter(x,y,150,marker='o',color='b')
                    self.canvas.draw()
        except queue.Empty:
            pass
        try:
            data = self.video_queue.get_nowait()
            decimg=cv2.imdecode(data,1)
            cv2image = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image.imgtk = imgtk
            self.image.configure(image=imgtk)
            self.fenetre.update()
        except queue.Empty:
            pass
        self.fenetre.after(50, self.update)

    #envoyer des coordonnées
    def envoyer_pos(self):
        deg_lat=self.msg_deg_lat.get()
        deg_long=self.msg_deg_long.get()
        wp = str(deg_lat)+';'+str(deg_long)
        self.send_queue.put("ADDWAY"+wp)
        self.send_queue.put("GO")

    def quit(self):
        self.send_queue.put("END")
        self.fenetre.quit()
        self.fenetre.destroy()

    def clear_waypoint(self):
        self.mapplot.remove()
        self.waypoint = []
        self.canvas.draw()
        self.mapplot = None

    def launch(self):
        if len(self.waypoint) != 0:
            print(self.waypoint)
            for pos in self.waypoint:
                self.send_queue.put("ADDWAY"+str(pos[1])+';'+str(pos[0]))
            self.send_queue.put("GO")
        pass

    def land(self):
        self.send_queue.put("LAND")

    def takeoff(self):
        self.send_queue.put("SIMPLETAKEOFF")
