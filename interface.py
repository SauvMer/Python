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
    a=msg.get() 
    print(a)
    file = open ("/home23/taillifa/Documents/ENSI 2/SAUVMER/test.txt","w")
    file.write(str(a)) 
    file.close()
    zone_emission.delete(0,END)
    zone_reception.delete("1.0", END)

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

    msg = StringVar()
    zone_emission= Entry(l_pos,background='white',textvariable=msg)
    zone_emission.grid(row = 1, column = 0)
    bouton_envoyer = Button(l_pos, text= "Envoyer les coordonnées", command = envoyer_pos)
    bouton_envoyer.grid(row=1, column=1)
    

    bouton=Button(fenetre, text="Fermer", command=fenetre.destroy) #Bouton qui détruit la fenêtre 
    bouton.pack(side =BOTTOM, padx =1, pady = 1) #insère le bouton dans la boucle
    print(msg)
    
#lance la boucle principale
    fenetre.mainloop() 
    