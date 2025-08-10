#!usr/bin/python3
import tkinter
import pyopengltk
import vertexus
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

#Dimensions de base de la fenetre...
LONGUEUR = 1200
HAUTEUR = 520

class Liste_des_vertex(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(width=int(LONGUEUR/2),height=HAUTEUR,bg="green")
        self.grid(row=0,column=2)
        self.liste_conteneur = tkinter.Listbox(self,bg="magenta",height=25,width=37)
        self.liste_conteneur.pack(side=tkinter.TOP)

    
class Tableau_de_bord(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(width=int(LONGUEUR/4),height=HAUTEUR,bg="yellow")
        self.grid(row=0,column=0)

class Visionneur_Tridimensionnel(OpenGLFrame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(width=int(LONGUEUR/2),height=HAUTEUR,bg="blue")
        self.grid(row=0,column=1)

    def initgl(self):
        GL.glLoadIdentity()
        GL.glClearColor(0,0,0,255)
        GLU.gluPerspective( 45 , (self.width/self.height) , 0.1 , 50 )
        GL.glTranslatef(0.0,0.0,-5)

    def redraw(self):
        pass

class FenetrePrincipale(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(bg="red")
        self.pack(expand=True,fill=tkinter.BOTH)
        self.TDB1 = Tableau_de_bord(self)
        self.VT1 = Visionneur_Tridimensionnel(self)
        self.LDV1 = Liste_des_vertex(self)
        self.mode = None # Le mode de la fenetre...

    def reaction_clavier_relache(self,event):
        if event.keysym == 'i':
            self.mode = "INSERTION"
        elif event.keysym == 'v':
            self.mode = "VISUAL"
        elif event.keysym == "Escape":
            self.mode = None
        #self.mise_a_jour_label_mode()

    def reaction_clavier_appui(self,event):
        if self.mode == "INSERTION":
            pass
        elif self.mode == "VISUAL":
            pass
        # Dans tous les cas, on peut déplacer le curseur...
        # deplacer_curseur...

def main():
    root = tkinter.Tk()
    root.title("Schema Designer v0.1")
    root.geometry(str(LONGUEUR)+"x"+str(HAUTEUR))
    root.resizable(False,False)
    FP1 = FenetrePrincipale(root)
    root.bind('<Key>',FP1.reaction_clavier_appui)
    root.bind('<KeyRelease>',FP1.reaction_clavier_relache)
    root.mainloop()

main()
