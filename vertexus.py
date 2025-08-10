#!usr/bin/python3

class vertex_specification:

    def __init__(self,x_init,y_init,z_init,taille_historique=10):
        try:
            self.pos_x = x_init
            self.pos_y = y_init
            self.pos_z = z_init
            self.taille_historique = taille_historique
            self.historique = []
            self.historique.append( (x_init,y_init,z_init)  )
        except TypeError as TE:
            print("Erreur de type : " + str(TE))
            print("Échec de création du vertex :(")

    def position_array(self):
        return [self.pos_x,self.pos_y,self.pos_z]

    def nouvelle_position(self,nouv_x,nouv_y,nouv_z,memoire=True):
        try:
            if memoire:
                self.historique.append( (nouv_x,nouv_y,nouv_z)  )
            self.pos_x = nouv_x 
            self.pos_y = nouv_y
            self.pos_z = nouv_z
        except Exception as erreur:
            print("!!! vertex_specification.nouvelle_position : "+str(erreur))

    def stringification(self):
        return "VERTEX:{}/{}/{}".format(int(self.pos_x),int(self.pos_y),int(self.pos_z))
        
       

def main():
    vertex1 = vertex_specification(1,2,4)
    print(vertex1.stringification())

if __name__ == "__main__":
    main()
