from vpython import *
import numpy as np
from funcion import objeto
from stl import mesh

scene.title = "<b>A bird is flying</b></n>\n"
#Ajustamos tamaño de pantalla
scene.width = 640
scene.height = 600
scene.forward = vector(0,-.3,-1)

running=True

def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Run"

button(text="Pause", pos=scene.title_anchor, bind=Run)

#Parametros base
r = 50
omega = 5
t = np.linspace(0,10,1001)
v_z = r/10	
beta = np.pi/4

# Pajaro creado
gaviota = objeto(mesh.Mesh.from_file('bird.stl'))
gaviota.set_pos(vector(r,0,2*r))
gaviota.rotar_x(np.pi,gaviota.cdg)
gaviota.rotar_y(np.pi-beta,gaviota.cdg)
gaviota2 = sphere(pos=gaviota.cdg, radius=r/100, color=color.red,
		make_trail=True, interval=1)	

#Vectores unitarios
x_i = arrow(pos=vector(0,0,0), axis=vector(1,0,0)*r/4, color=color.red)
y_j = arrow(pos=vector(0,0,0), axis=vector(0,1,0)*r/4, color=color.blue)
z_k = arrow(pos=vector(0,0,0), axis=vector(0,0,1)*r/4, color=color.green)

#Vectores de trayectoria con sus respectivas letras
rarr = arrow(pos=gaviota.cdg, axis=vector(1,0,0), color=color.magenta)
txt_rarr = text(text='n', pos=rarr.pos+rarr.axis, axis=rarr.axis, align='center', height=0.4,
          color=color.magenta, billboard=True, emissive=True)

tarr = arrow(pos=gaviota.cdg, axis=vector(0,1,0)*r/4, color=color.white)
txt_tarr = text(text='t', pos=tarr.pos+tarr.axis, axis=tarr.axis, align='center', height=0.4,
          color=color.white, billboard=True, emissive=True)

Larr = arrow(pos=gaviota.cdg, axis=np.sin(beta)*rarr.axis
								+np.cos(beta)*z_k.axis,
			color=color.orange)
txt_Larr = text(text='L', pos=Larr.pos+Larr.axis, axis=Larr.axis, align='center', height=0.4,
          color=color.orange, billboard=True, emissive=True)


scene.autoscale = True

# aqui escribimos la descripcion del video
scene.append_to_caption(
"""\n	Una gaviota puede planear, a pesar de la gravedad, 
	gracias a una fuerza de origen aerodinamico, 
	conocida como fuerza de sustentacion, L.
	El movimiento es descrito en esta representacion visual""")


while True:
	for this_t in t:
		#Actualiza la posicion de la gaviota
		#y la direccion de los vectores unitarios r, theta
		rate(50)  # Espera 1/60 s para que no se vea tan rapido
		theta = omega*this_t

		# actualiza la direccion de r y theta
		rarr.axis = vector(np.cos(theta),np.sin(theta),0)
		tarr.axis = vector(-np.sin(theta), np.cos(theta), 0)
		Larr.axis = -np.sin(beta)*rarr.axis + np.cos(beta)*z_k.axis	

		# actualiza la direccion de r, theta y la gaviota
		Larr.pos = rarr.pos = tarr.pos  = gaviota2.pos = vector(r*np.cos(theta), r*np.sin(theta),
			2*r-v_z*this_t)

		gaviota.rotar_z(omega*(t[1]-t[0]), vector(0,0,0))
		gaviota.set_pos(gaviota.cdg+vector(0,0,-v_z*t[1]-t[0]))		
			
		#generamos las letras
		txt_rarr.pos = rarr.pos+rarr.axis
		txt_tarr.pos = tarr.pos+tarr.axis
		txt_Larr.pos = Larr.pos+Larr.axis
	reset = input('Press any key to reset')
