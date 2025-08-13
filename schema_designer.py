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
        self.configure(bg="green")
        self.pack(side=tkinter.LEFT,expand=True,fill=tkinter.BOTH)
        self.liste_conteneur = tkinter.Listbox(self)
        self.liste_conteneur.pack(side=tkinter.TOP,expand=True,fill=tkinter.Y)
        self.liste_de_vertex = []

    def mettre_listbox_a_jour(self):
        self.liste_conteneur.delete(0,tkinter.END)
        for vertex in self.liste_de_vertex:
            self.liste_conteneur.insert(tkinter.END,vertex)

    def inserer_vertex(self,vertex_insertion):
        self.liste_de_vertex.append(vertex_insertion.position_array())
        self.mettre_listbox_a_jour()
        print("Insertion vertex reussie!!!")

    
class Tableau_de_bord(tkinter.Frame):

    def __init__(self,master):

        super().__init__(master)
        self.configure(bg="pink")
        self.pack(side=tkinter.LEFT,expand=True,fill=tkinter.Y)

        self.label_mode = tkinter.Label(self,text="MODE:???")
        self.label_mode.pack()

        self.label_position_curseur = tkinter.Label(self,text="CURSEUR> X:? Y:? Z:?")
        self.label_position_curseur.pack()

class Visionneur_Tridimensionnel(OpenGLFrame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(width=int(LONGUEUR/2),height=HAUTEUR,bg="blue")
        self.pack(side=tkinter.LEFT)

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
        self.configure(bg="gainsboro")
        self.pack(expand=True,fill=tkinter.BOTH)
        self.TDB1 = Tableau_de_bord(self)
        self.VT1 = Visionneur_Tridimensionnel(self)
        self.LDV1 = Liste_des_vertex(self)
        self.mode = None # Le mode de la fenetre...
        self.vertex_curseur = vertexus.vertex_specification(0,0,0)

    def reaction_clavier_relache(self,event):
        if event.keysym == 'q':
            self.mode = "INSERTION"
            self.TDB1.label_mode.configure(text="MODE:"+self.mode)
        elif event.keysym == 'w':
            self.mode = "VISUEL"
            self.TDB1.label_mode.configure(text="MODE:"+self.mode)
        elif event.keysym == "Escape":
            self.mode = "VIDE"
            self.TDB1.label_mode.configure(text="MODE:"+self.mode)
        

    def reaction_clavier_appui(self,event):
        print(event)
        if self.mode == "INSERTION":
            if event.keysym == "space":
                self.LDV1.inserer_vertex(self.vertex_curseur)
        # Dans tous les cas, on peut déplacer le curseur...
        # Changement de position selon l'axe X
        if event.keysym == 'u':
            self.vertex_curseur.nouvelle_position(self.vertex_curseur.pos_x+1,self.vertex_curseur.pos_y,self.vertex_curseur.pos_z)
        elif event.keysym == 'j':
            self.vertex_curseur.nouvelle_position(self.vertex_curseur.pos_x-1,self.vertex_curseur.pos_y,self.vertex_curseur.pos_z)
        # Changement de position selon l'axe Y
        elif event.keysym == 'i':
            self.vertex_curseur.nouvelle_position(self.vertex_curseur.pos_x,self.vertex_curseur.pos_y+1,self.vertex_curseur.pos_z)
        elif event.keysym == 'k':
            self.vertex_curseur.nouvelle_position(self.vertex_curseur.pos_x,self.vertex_curseur.pos_y-1,self.vertex_curseur.pos_z)
        # Changement de position selon l'axe Z
        elif event.keysym == 'o':
            self.vertex_curseur.nouvelle_position(self.vertex_curseur.pos_x,self.vertex_curseur.pos_y,self.vertex_curseur.pos_z+1)
        elif event.keysym == 'l':
            self.vertex_curseur.nouvelle_position(self.vertex_curseur.pos_x,self.vertex_curseur.pos_y,self.vertex_curseur.pos_z-1)
        self.TDB1.label_position_curseur.configure(text="CURSEUR> X:{} Y:{} Z:{}".format(self.vertex_curseur.pos_x,self.vertex_curseur.pos_y,self.vertex_curseur.pos_z))

    def arret_application(self,event):
        self.master.destroy()


def main():
    root = tkinter.Tk()
    root.title("Schema Designer v0.1")
    root.geometry(str(LONGUEUR)+"x"+str(HAUTEUR))
    root.resizable(False,False)
    FP1 = FenetrePrincipale(root)
    root.bind('<Key>',FP1.reaction_clavier_appui)
    root.bind('<KeyRelease>',FP1.reaction_clavier_relache)
    root.bind(':A',FP1.arret_application)
    root.mainloop()

main()
