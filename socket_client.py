#!/usr/bin/python
import tkinter
import socket
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

def tentative_connexion(surnom,adresse):
    print("Surnom : " + surnom)
    print("Adresse : " + adresse)

def quitter_application(event):
    root.destroy()

class FenetreConnexion(tkinter.Toplevel):

    def __init__(self,master):

        # Informations générales sur une fenêtre de connexion...
        super().__init__(master)
        self.title("Connexion")
        self.configure(width=600,height=300,background="red")
        self.resizable(False,False)

        # Les widgets d'une fenêtre de connexion...
        self.label_surnom = tkinter.Label(self,text="Surnom : ")
        self.label_adresse = tkinter.Label(self,text="Adresse du serveur : ")

        self.surnom_saisi = tkinter.StringVar()
        self.adresse_saisie = tkinter.StringVar()
        self.texte_surnom = tkinter.Entry(self,textvariable=self.surnom_saisi)
        self.texte_adresse = tkinter.Entry(self,textvariable=self.adresse_saisie)

        self.label_surnom.grid(row=0,column=0,padx=20,pady=20)
        self.label_adresse.grid(row=1,column=0,padx=20,pady=20)

        self.texte_surnom.grid(row=0,column=1,padx=20,pady=20)
        self.texte_adresse.grid(row=1,column=1,padx=20,pady=20)

        self.bouton_connexion = tkinter.Button(self,text="Connexion", command = lambda : tentative_connexion(self.surnom_saisi.get(),self.adresse_saisie.get()) )
        self.bouton_connexion.grid(row=2,column=0,columnspan=2,padx=20,pady=20)
   
class FenetrePrincipale(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(background="green")
        self.pack(expand=True,fill=tkinter.BOTH)

        self.TDB1 = TableauDeBord(self)
        self.SHOWER1 = Shower(self)
        self.SHOWER1.configure(width=400,height=500)
        self.SHOWER1.animate = 10
        self.SHOWER1.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)


class TableauDeBord(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(background="red",width=200)
        self.pack(expand=True,fill=tkinter.Y,side=tkinter.LEFT)
        
        self.bouton_connexion = tkinter.Button(self,text="Partie multijoueur",width=20)
        self.bouton_connexion.grid(row=0,column=0,ipadx=5,ipady=5,padx=10,pady=10)
        self.bouton_connexion.bind('<Button>',self.tenter_une_connexion)

        self.bouton_quitter = tkinter.Button(self,text="Quitter",width=20)
        self.bouton_quitter.grid(row=1,column=0,ipadx=5,ipady=5,padx=10,pady=10)
        self.bouton_quitter.bind('<Button>',quitter_application)

        self.label_position_surnom = tkinter.Label(self,text="Surnom : ???")
        self.label_position_surnom.grid(row=2,column=0,ipady=5,padx=10,pady=10)

        self.label_position_x = tkinter.Label(self,text="Position X : ???")
        self.label_position_x.grid(row=3,column=0,ipady=5,padx=10,pady=10)

        self.label_position_z = tkinter.Label(self,text="Position Z : ???")
        self.label_position_z.grid(row=4,column=0,ipady=5,padx=10,pady=10)

    def tenter_une_connexion(self,event):
        FC1 = FenetreConnexion(root) 

def main():
   
    FP1 = FenetrePrincipale(root)

    root.mainloop()

main()
