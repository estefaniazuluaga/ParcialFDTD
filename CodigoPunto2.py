import numpy as np
from math import exp
import scipy.constants as sc
from matplotlib import pyplot as plt

# Definiciones

Npts = 200   # Número de celdas 3m/dx

# Vectores vacíos para el campo eléctrico y magnético
Ez = np.zeros((1,Npts),dtype=float)  
Hy = np.zeros((1,Npts),dtype=float)

dx = 0.015  # Se seleccionó un dx con base al criterio dado
dt = dx / 3e8

lb = 0.3  # Valor de lambda
e_rm = 2  # Epsilon relativo del material dieléctrico
d = lb / (4 * np.sqrt(e_rm)) # Espesor (cambia según el número que multiplique a la raíz)


d_ini = 100 # Punto inicial material dieléctrico
d_fin = d_ini + int(round(d / dx)) # Punto final placa (depende de 'd')


# Asignación de epsilon correspondiente a cada medio
ei = np.zeros((1,Npts),dtype=float)
ei[0, 0: d_ini] = sc.epsilon_0
ei[0, d_ini: d_fin] = sc.epsilon_0 * 2
ei[0, d_fin: 200]=sc.epsilon_0 * 4

ui = np.zeros((1,Npts),dtype=float)
ui[0, 0: 200]=sc.mu_0


a=0
b=0
f = 1e9  # f = c/lambda
tau = 16 # tau = 8 ns / dt


x = np.linspace(0, Npts, num=Npts) * dx
Ez = np.zeros((1,Npts),dtype=float)
Hy = np.zeros((1,Npts),dtype=float)


# Pulso gaussiano aplicado en un punto i 
for i in range(0, 200):
    Ez[0, i] = np.exp(-(i - 3 * tau) ** 2 / (tau) ** 2)
    
y = Ez[0,:]
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-')
ax.axvline(x=d_ini * dx, color='b')
ax.axvline(x=d_fin * dx, color='c')
ax.set_xlim(0,200 * dx)
ax.set_ylim(-0.5,1.5)
ax.set_ylabel('Campo eléctrico(V/m)')
ax.set_xlabel('Posición x(m)')
for i in range(0, 110): 
    # Campo magnético
    for j in range(0, (Npts - 1)):
        Hy[0, j] = Hy[0,j] + (dt / (ui[0,j] * dx)) * (Ez[0,j+1] - Ez[0,j])
    # Campo eléctrico
    for k in range(1, Npts):
        Ez[0, k] = Ez[0,k] + (dt / (ei[0,k] * dx)) * (Hy[0,k] - Hy[0,k-1])

    # Condiciones de frontera absorbente
    Ez[0,0] = 0
    Ez[0,Npts-1] = 0
    Hy[0,0] = 0
    Hy[0,Npts-1] = 0
    line1.set_ydata(Ez[0,:])
    fig.canvas.draw()#####actualizacion de la grafica
    fig.canvas.flush_events()
    
# Imprimir amplitud y coeficientes de reflexión y tramitancia
print(max(Ez[0, :]))
max(Ez[0, :])
print("Coef reflexion:" + str(min(Ez[0, :]) / 0.5) + " Coef transmitancia " + str(max(Ez[0, :]) / 0.5))
