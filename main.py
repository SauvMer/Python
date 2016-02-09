from tkinter import *
from tkinter.messagebox import *

def printTest():
    label = Label(fenetre, text=value.get())
    label.pack()

def callback():
    if askyesno('Titre 1', 'Êtes-vous sûr de vouloir faire ça?'):
        showwarning('Titre 2', 'Tant pis...')
    else:
        showinfo('Titre 3', 'Vous avez peur!')
        showerror("Titre 4", "Aha")

if __name__=='__main__':
    fenetre = Tk()
    fenetre.wm_title("Nom de la fenetre")

    label = Label(fenetre, text='Fist Window')
    label.pack()

    # Bouton
    bouton=Button(fenetre, text="print test", command=callback)
    bouton.pack()

    # Input
    value = StringVar()
    value.set("empty")
    entree = Entry(fenetre, textvariable=value, width=30)
    entree.pack()

    # Affichage d'image
    photo = PhotoImage(file="drone_snow.png")


    canvas = Canvas(fenetre,width=400, height=400)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.pack()

    fenetre.geometry('{}x{}'.format(800, 800))
    fenetre.mainloop()
