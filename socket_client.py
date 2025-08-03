#!/usr/bin/python
import tkinter
import pyopengltk
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

root = tkinter.Tk()
root.geometry("800x500")
root.title("Client test")
root.resizable(False,False)

class Shower(OpenGLFrame):
    def initgl(self):
        GL.glLoadIdentity()
        GL.glClearColor(0,0,0,255)
        GLU.gluPerspective( 45 , (self.width/self.height) , 0.1 , 50 )
        GL.glTranslatef(0.0,0.0,-5)
    def redraw(self):
        pass

def creer_fenetre_connexion(event):
    
    fenetre_connexion = tkinter.Toplevel()
    fenetre_connexion.title("Connexion")
    fenetre_connexion.configure(width=600,height=300,background="red")
    fenetre_connexion.resizable(False,False)

    label_surnom = tkinter.Label(fenetre_connexion,text="Surnom : ")
    label_adresse = tkinter.Label(fenetre_connexion,text="Adresse du serveur : ")

    texte_surnom = tkinter.Entry(fenetre_connexion)
    texte_adresse = tkinter.Entry(fenetre_connexion)

    label_surnom.grid(row=0,column=0,padx=20,pady=20)
    label_adresse.grid(row=1,column=0,padx=20,pady=20)

    texte_surnom.grid(row=0,column=1,padx=20,pady=20)
    texte_adresse.grid(row=1,column=1,padx=20,pady=20)

    bouton_connexion = tkinter.Button(fenetre_connexion,text="Connexion")
    bouton_connexion.grid(row=2,column=0,columnspan=2,padx=20,pady=20)

def quitter_application(event):
    root.destroy()

def main():
    
    frame_principale = tkinter.Frame(root)
    frame_principale.configure(background="gray")
    frame_principale.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)
 
    frame3D = Shower(root)
    frame3D.configure(width=400,height=500)
    frame3D.animate = 10
    frame3D.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)
 
    bouton_connexion = tkinter.Button(frame_principale,text="Partie multijoueur",width=20)
    bouton_connexion.grid(row=0,column=0,ipadx=5,ipady=5,padx=10,pady=10)
    bouton_connexion.bind('<Button>',creer_fenetre_connexion)

    bouton_quitter = tkinter.Button(frame_principale,text="Quitter",width=20)
    bouton_quitter.grid(row=1,column=0,ipadx=5,ipady=5,padx=10,pady=10)
    bouton_quitter.bind('<Button>',quitter_application)

    label_position_surnom = tkinter.Label(frame_principale,text="Surnom : ???")
    label_position_surnom.grid(row=2,column=0,ipady=5,padx=10,pady=10)

    label_position_x = tkinter.Label(frame_principale,text="Position X : ???")
    label_position_x.grid(row=3,column=0,ipady=5,padx=10,pady=10)

    label_position_z = tkinter.Label(frame_principale,text="Position Z : ???")
    label_position_z.grid(row=4,column=0,ipady=5,padx=10,pady=10)


    root.mainloop()

main()
