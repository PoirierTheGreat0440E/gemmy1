#!/usr/bin/python
import tkinter
import pyopengltk
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

class Shower(OpenGLFrame):
    def initgl(self):
        GL.glLoadIdentity()
        GL.glClearColor(0,0,0,255)
        GLU.gluPerspective( 45 , (self.width/self.height) , 0.1 , 50 )
        GL.glTranslatef(0.0,0.0,-5)
    def redraw(self):
        pass

def main():

    root = tkinter.Tk()
    root.geometry("800x500")
    root.title("Client test")
    root.resizable(False,False)
    
    frame_principale = tkinter.Frame(root)
    frame_principale.configure(background="gray")
    frame_principale.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)
 
    frame3D = Shower(root)
    frame3D.configure(width=400,height=500)
    frame3D.animate = 10
    frame3D.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)

   
    bouton_connexion = tkinter.Button(frame_principale,text="Partie multijoueur",width=20)
    bouton_connexion.grid(row=0,column=0,ipadx=5,ipady=5,padx=10,pady=10)

    bouton_quitter = tkinter.Button(frame_principale,text="Quitter",width=20)
    bouton_quitter.grid(row=1,column=0,ipadx=5,ipady=5,padx=10,pady=10)

    label_position_surnom = tkinter.Label(frame_principale,text="Surnom : ???")
    label_position_surnom.grid(row=2,column=0,ipady=5,padx=10,pady=10)

    label_position_x = tkinter.Label(frame_principale,text="Position X : ???")
    label_position_x.grid(row=3,column=0,ipady=5,padx=10,pady=10)

    label_position_z = tkinter.Label(frame_principale,text="Position Z : ???")
    label_position_z.grid(row=4,column=0,ipady=5,padx=10,pady=10)


    root.mainloop()

main()
