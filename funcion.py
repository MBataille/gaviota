from stl import mesh
from vpython import *
import numpy as np
#la idea es que 'malla' sea un archivo stl, eso se logra importando un archivo con mesh.Mesh.from_file('nombrearchivo')
#y asignandolo a una variable que luego sería la entrada de la función crear_desde_stl

class objeto():
    def __init__(self,malla,color):
        self.tris=[]
        self.I=malla.get_mass_properties()[2]
        self.v0=malla.v0
        self.v1=malla.v1
        self.v2=malla.v2
        self.color = color
        self.normales=malla.normals
        self.init_pos(vector(malla.get_mass_properties()[1][0],malla.get_mass_properties()[1][1],malla.get_mass_properties()[1][2]))

    def init_pos(self,v):
        '''vector de vpython entra, actualiza pos cdg'''
        self.cdg=v
        for n in range(len(self.v1)):
            normalActual = vec(self.normales[n][0], self.normales[n][1], self.normales[n][2])
            a = vertex(pos=vec(self.v0[n][0] - self.cdg.x, self.v0[n][1] - self.cdg.y, self.v0[n][2] - self.cdg.z),color=color.red, normal=normalActual)
            b = vertex(pos=vec(self.v1[n][0] - self.cdg.x, self.v1[n][1] - self.cdg.y, self.v1[n][2] - self.cdg.z),color=color.red, normal=normalActual)
            c = vertex(pos=vec(self.v2[n][0] - self.cdg.x, self.v2[n][1] - self.cdg.y, self.v2[n][2] - self.cdg.z),color=color.red, normal=normalActual)
            a.color = self.color
            b.color = self.color
            c.color = self.color
            self.tris.append(triangle(vs=[a,b,c]))  # esto toma los vertex para hacer un triangulo y los agrega a la lista que originalmente estaba vacía

    def set_pos(self,v):
        '''vector de vpython entra, actualiza pos cdg'''
        v_prev=self.cdg
        self.cdg=v


        for triangulo in self.tris:
            triangulo.v0.pos+=v-v_prev
            triangulo.v1.pos+=v-v_prev
            triangulo.v2.pos+=v-v_prev


    def multiplicar_matriz_vec(self,matriz, vecc):
        vecnp = np.array([vecc.x, vecc.y, vecc.z])
        out = matriz.dot(vecnp)
        return vec(out[0], out[1], out[2])


    def rotar_x(self, theta, v):
        matrizRot = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
        for triangulo in self.tris:
            triangulo.v0.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v0.pos-v)+v
            triangulo.v1.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v1.pos-v)+v
            triangulo.v2.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v2.pos-v)+v


    def rotar_y(self, theta, v):
        matrizRot = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
        for triangulo in self.tris:
            triangulo.v0.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v0.pos-v)+v
            triangulo.v1.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v1.pos-v)+v
            triangulo.v2.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v2.pos-v)+v

    def rotar_z(self, theta, v):
        matrizRot = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
        for triangulo in self.tris:
            triangulo.v0.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v0.pos-v)+v
            triangulo.v1.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v1.pos-v)+v
            triangulo.v2.pos=self.multiplicar_matriz_vec(matrizRot,triangulo.v2.pos-v)+v

###########################################################################################




# XWING=objeto(xwing)
# omega=3
# dt=.01
# t=0
# R=50
# while True:
#     rate(100)
#     XWING.set_pos(R*vec(np.cos(omega*t),np.sin(omega*t),0))

#     XWING.rotar_z(5*omega*dt, XWING.cdg)

#     t+=dt