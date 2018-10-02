# Main Simulador Filtro de Particulas en 2D

from math import *
import random
import matplotlib.pyplot as plt
import PlotClass
from RobotSim import RobotSim

# (x,y) maximo del mapa
world_x = 100
world_y = 100

n_particulas = 300 # Numero de particulas

obstaculos = [] 
n_obstaculos = 20 # Numero de obstaculos
steps = 30  # Numero de iteraciones

for i in range(n_obstaculos):
  obstaculos.append([random.randint(1, world_x), random.randint(1, world_y)])

# Movimiento de las particulas
def predict(particulas, n_particulas):
    p2 = []
    for i in range(n_particulas):
        p2.append( particulas[i].move(0.1, 2.) )
    return p2

def resample(weights, particulas, n_particulas):
    p3 = []
    index = int(random.random() * n_particulas)
    c_sum = 0.0
    # Particula con mayor peso
    particula_mayor_peso = max(weights)

    # Escalamiento respecto a la particula de mayo peso
    for i in range(n_particulas):
        c_sum += random.random() * particula_mayor_peso
        while c_sum > weights[index]:
            c_sum -= weights[index]
            index = (index + 1) % n_particulas
        p3.append(particulas[index])
    return p3

def main():

    robot = RobotSim(world_x,world_y,obstaculos)
    robot = robot.move(0.1, 2.)
    scan = robot.sensor_laser()

    particulas = []

    for i in range(n_particulas):
        robot = RobotSim(world_x,world_y,obstaculos)
        robot.set_noise(0.05, 0.08, 5.0)
        particulas.append(robot)

    # Movimientos
    for t in range(steps):
        robot = robot.move(0.1, 2.)
        scan = robot.sensor_laser()

        # Etapa de Prediccion
        p2 = predict(particulas, n_particulas)
        particulas = p2

        # Peso de las particulas del filtro respecto a la
        # lectura de datos del robot en el mapa 
        weights = []
        for i in range(n_particulas):
            weights.append(particulas[i].update(scan))

        # Resampleado
        p3 = resample(weights, particulas, n_particulas)
        
        # Particulas relocalizadas segun el resampleado
        particulas = p3
        # Plot
        PlotClass.visualization(robot, t, p2, p3, weights, world_x,world_y, obstaculos)

    print 'Array de particulas = ', particulas # Muestra el arreglo de particulas

if __name__ == "__main__":
    main()  
  

