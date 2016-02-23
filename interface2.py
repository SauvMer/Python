#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import * 
from tkinter.filedialog import *



#https://fr.wikibooks.org/wiki/Programmation_Python/Tkinter
#from tkinter.messagebox import *


#recevoir les coordonnées
def afficher_pos():  
    fichier = open("test.txt", "r")
    content= fichier.read()
    zone_reception.insert(INSERT, content)
    #zone_reception.create_text(200,25,anchor= E, text=content) 
    #zone_reception.delete("all") 
    fichier.close()

#envoyer des coordonnées
def envoyer_pos():
    deg_lat=msg_deg_lat.get()
    min_lat=msg_min_lat.get()
    sec_lat=msg_sec_lat.get()
    deg_long=msg_deg_long.get()
    min_long=msg_min_long.get()
    sec_long=msg_sec_long.get() 
    if identifier(deg_lat) & identifier(min_lat) & identifier(sec_lat) :
        if identifier(deg_long) & identifier(min_long) & identifier(sec_long):
            print(deg_lat,min_lat,sec_lat,value_lat.get(),deg_long,min_long,sec_long,value_long.get())
            file = open ("test.txt","w")
            file.write(str(deg_lat)+','+str(min_lat) + ',' + str(sec_lat)+','+str(value_lat.get())+ ','+ str(deg_long)+','+str(min_long) + ',' + str(sec_long)+','+str(value_long.get())) 
            file.close()
        
    zone_deg_lat.delete(0,END)
    zone_sec_lat.delete(0,END)
    zone_min_lat.delete(0,END)
    zone_deg_long.delete(0,END)
    zone_sec_long.delete(0,END)
    zone_min_long.delete(0,END)
    zone_reception.delete("1.0", END)

#identifier le format des coordonnées
def identifier(msg):
    liste=['0','1','2','3','4','5','6','7','8','9']
    i=0
    for i in range(len(msg)):
        if msg[i] in liste:
            print("coordonnées correctes")
            return True
        else:
            print("erreur de formatage de coordonnées")
            return False
    
if __name__ == '__main__':
    
    #Gestion de la fenetre
    fenetre = Tk() #création de la fenêtre, nom au choix
    fenetre.title("Centre de contrôle SAUVMER") #nom de la fenetre
    fenetre['bg']='white'
    FWidth=fenetre.winfo_screenwidth()
    FHeight=fenetre.winfo_screenheight()
    label = Label(fenetre, text="Bienvenue au centre de contrôle SAUVMER")
    label['fg']='blue' #création du texte de couleur bleue
    label['bg']='white' #couleur fond de texte
    label.pack()#insère le texte dans la fenetre


    #case envoyer & recevoir data coordonnees
    l_pos = LabelFrame(fenetre, text="Positionnement du drone", padx=20, pady=20)
    l_pos.pack(fill="both", expand="yes")

    bouton_coord= Button (l_pos, text="Obtenir les coordonnées", command=afficher_pos)
    bouton_coord.grid(row=0,column=0)

    #zone_reception = Canvas(l_pos,width=200, height= 25,background='white') #Définit les dimensions du canevas
    zone_reception = Text(l_pos,width=25, height= 1,background='white')
    zone_reception.grid(row= 0, column =1) #Affiche le canevas

    # label latitude
    label_lat = Label(l_pos, text="Latitude")
    label_lat.grid(row= 1, column =0)

    # label longitude
    label_long = Label(l_pos, text="Longitude")
    label_long.grid(row= 2, column =0)

    #bouton radio Nord et Sud
    value_lat = StringVar()
    bouton1 = Radiobutton(l_pos, text="N", variable=value_lat, value='N')
    bouton2 = Radiobutton(l_pos, text="S", variable=value_lat, value='S')
    bouton1.grid(row= 1, column =7)
    bouton2.grid(row= 1, column =8)

    #bouton radio Est et Ouest
    value_long = StringVar()
    bouton3 = Radiobutton(l_pos, text="O", variable=value_long, value='O')
    bouton4 = Radiobutton(l_pos, text="E", variable=value_long, value='E')
    bouton3.grid(row= 2, column =7)
    bouton4.grid(row= 2, column =8)

    #zones degré
    msg_deg_lat = StringVar()
    zone_deg_lat = Entry(l_pos,background='white',textvariable=msg_deg_lat)
    zone_deg_lat.grid(row = 1, column = 1)
    msg_deg_long = StringVar()
    zone_deg_long = Entry(l_pos,background='white',textvariable=msg_deg_long)
    zone_deg_long.grid(row = 2, column = 1)

    #label degré
    label_deg_lat=Label(l_pos, text='°')
    label_deg_lat.grid(row=1,column = 2)
    label_deg_long=Label(l_pos, text='°')
    label_deg_long.grid(row=2,column = 2)

    #zones minutes
    msg_min_lat = StringVar()
    zone_min_lat = Entry(l_pos,background='white',textvariable=msg_min_lat)
    zone_min_lat.grid(row = 1, column = 3)
    msg_min_long = StringVar()
    zone_min_long = Entry(l_pos,background='white',textvariable=msg_min_long)
    zone_min_long.grid(row = 2, column = 3)

    #label minutes
    label_min_lat=Label(l_pos, text="'")
    label_min_lat.grid(row=1,column = 4)
    label_min_long=Label(l_pos, text="'")
    label_min_long.grid(row=2,column = 4)

    #zones secondes
    msg_sec_lat = StringVar()
    zone_sec_lat = Entry(l_pos,background='white',textvariable=msg_sec_lat)
    zone_sec_lat.grid(row = 1, column = 5)
    msg_sec_long = StringVar()
    zone_sec_long = Entry(l_pos,background='white',textvariable=msg_sec_long)
    zone_sec_long.grid(row = 2, column = 5)

    #label secondes
    label_sec_lat=Label(l_pos, text='\"')
    label_sec_lat.grid(row=1,column = 6)
    label_sec_long=Label(l_pos, text='\"')
    label_sec_long.grid(row=2,column = 6)

    #bouton envoie coordonnées
    bouton_envoyer = Button(l_pos, text= "Envoyer les coordonnées", command = envoyer_pos)
    bouton_envoyer.grid(row=1, column=9)

    #Bouton fermeture de la fenetre
    bouton=Button(fenetre, text="Fermer", command=fenetre.destroy) #Bouton qui détruit la fenêtre
    bouton.pack(side =BOTTOM, padx =1, pady = 1) #insère le bouton dans la boucle

    #lance la boucle principale
    fenetre.mainloop()
    