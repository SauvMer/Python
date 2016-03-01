from tkinter.filedialog import *
import queue
from threading import Thread
from time import sleep

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

class IHM():

    #recevoir les coordonnées
    def update(self):
        try:
            temp = self.queue.get_nowait()
            if(temp.startswith("GPS")):
                self.zone_reception.delete("1.0", END)
                self.zone_reception.insert(INSERT, temp[3:])
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
        self.fenetre['bg']='white'
        FWidth=self.fenetre.winfo_screenwidth()
        FHeight=self.fenetre.winfo_screenheight()
        label = Label(self.fenetre, text="Bienvenue au centre de contrôle SAUVMER")
        label['fg']='blue' #création du texte de couleur bleue
        label['bg']='white' #couleur fond de texte
        label.pack()#insère le texte dans la fenetre


        #case envoyer & recevoir data coordonnees
        l_pos = LabelFrame(self.fenetre, text="Positionnement du drone", padx=20, pady=20)
        l_pos.pack(fill="both", expand="yes")

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

        #Bouton fermeture de la fenetre
        bouton=Button(self.fenetre, text="Fermer", command=self.fenetre.destroy) #Bouton qui détruit la fenêtre
        bouton.pack(side =BOTTOM, padx =1, pady = 1) #insère le bouton dans la boucle

        self.update()