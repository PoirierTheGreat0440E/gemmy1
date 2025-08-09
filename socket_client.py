#!/usr/bin/python
import tkinter
import socket
import pyopengltk
import threading
import sched
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

        self.bouton_connexion = tkinter.Button(self,text="Connexion",command=self.tenter_connexion)
        self.bouton_connexion.grid(row=2,column=0,padx=20,pady=20)

        self.bouton_quitter = tkinter.Button(self,text="Annuler", command = lambda : self.destroy() )
        self.bouton_quitter.grid(row=2,column=1,padx=20,pady=20)
        

    def tenter_connexion(self):
        SURNOM = "GUEST"
        ADRESSE = "127.0.0.1"
        if  self.surnom_saisi.get().strip() != "":
            SURNOM = self.surnom_saisi.get()
        if  self.adresse_saisie.get().strip() != "":
            ADRESSE = adresse_saisie.get()
        PORT = 65000
        self.master.initier_communication(SURNOM,ADRESSE,PORT)
        

class FenetrePrincipale(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(background="white")
        self.pack(expand=True,fill=tkinter.BOTH)

        self.TDB1 = TableauDeBord(self)
        self.SHOWER1 = Shower(self)
        self.SHOWER1.configure(width=400,height=500)
        self.SHOWER1.animate = 10
        self.SHOWER1.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT)
        
       
class TableauDeBord(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.configure(background="gainsboro",width=200)
        self.pack(expand=True,fill=tkinter.Y,side=tkinter.LEFT)
        
        self.bouton_connexion = tkinter.Button(self,text="Partie multijoueur",width=20, command=self.creer_fenetre_connexion )
        self.bouton_connexion.grid(row=0,column=0,ipadx=5,ipady=5,padx=10,pady=10)
        #self.bouton_connexion.bind('<Button>',self.tenter_une_connexion)

        self.bouton_quitter = tkinter.Button(self,text="Quitter",width=20)
        self.bouton_quitter.grid(row=1,column=0,ipadx=5,ipady=5,padx=10,pady=10)
        self.bouton_quitter.bind('<Button>',quitter_application)
       
        # Connecteurs pour envoyer et écouter les messages...
        self.connecteur_envoi = socket.socket()
        self.connecteur_reception = socket.socket()
        self.id_reception = -1

        # Le thread utilisé pour communiquer avec le serveur
        self.recepteur = threading.Thread(target=self.reception_asynchrone)
        self.recepteur.daemon = True

        self.FC1 = None
       
    def creer_fenetre_connexion(self):
        self.FC1 = FenetreConnexion(self)

    def initier_communication(self,SURNOM,ADRESSE,PORT):
        self.FC1.destroy()
        print("Connection vers {}:{}".format(ADRESSE,PORT))
        try:
        
            # On commence par la connexion pour l'envoi des messages...
            print("Connexion ENVOI...")
            connexion_pour_envoi = self.connecteur_envoi.connect( (ADRESSE,PORT)  )
            self.id_reception = int(self.connecteur_envoi.recv(1024).decode("utf-8").strip())
            print("ID de reception : "+str(self.id_reception))

            # Maintenant que l'on a reçu l'id de réception, on peut le communiquer au serveur de réception...
            print("Connexion RECEPTION...")
            connexion_pour_reception = self.connecteur_reception.connect( (ADRESSE,PORT+1) )
            self.connecteur_reception.sendall( bytearray("id:"+str(self.id_reception)+"\n","utf-8") )
            
            print("PROCESSUS DE CONNEXION > OK")
           
            self.recepteur.start()
            #self.recepteur.join()
        
        except Exception as erreur:
            print("Connexion échouée !")
            print(erreur)

    def reception_asynchrone(self):        
        message_recu = ""
        while True:
            try:
                message_recu = self.connecteur_reception.recv(1024).decode("utf-8").strip()
                if message_recu == "endcommunication":
                    self.deconnexion()            
                    break
                print(">>> Reception : " + message_recu)
            except Exception as erreur_reception:
                print("ERR RECEPTION > "+str(erreur_reception))
        print("Reception asynchrone terminee !")
    
    def react_to_key(self,event):
        try:
            self.connecteur_envoi.sendall( bytearray(event.keysym+"\n","utf-8") )
            if event.keysym == 'q':
                self.connecteur_envoi.sendall(  bytearray("endfromclient\n","utf-8") )
        except Exception as erreur:
            #print("ERR ENVOI > "+str(event))
            pass

    def deconnexion(self):
        self.connecteur_reception.close()
        self.connecteur_envoi.close()
        print("Déconnexion réussie !")

    
def main():
   
    FP1 = FenetrePrincipale(root)
    root.bind('<Key>',FP1.TDB1.react_to_key)
    root.mainloop()

main()
