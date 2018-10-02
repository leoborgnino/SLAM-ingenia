# Clase que simula un robot/particula, su posicion (x,y,theta),
# su movimiento, ruido en el sensado y movimiento.

from math import *
import random

class RobotSim:
    def __init__(self,world_x,world_y,obstaculos):
        self.obstaculos = obstaculos
        self.max_world_x = world_x
        self.max_world_y = world_y
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0
        # posicion inicial (x,y,theta)
        self.x = random.random() * self.max_world_x
        self.y = random.random() * self.max_world_y
        self.orientation = random.random() * 2.0 * pi


    # Setear el ruido en el movimiento de traslacion, de rotacion y de los sensores
    def set_noise(self, new_forward_noise, new_turn_noise, new_sense_noise):
        self.forward_noise = float(new_forward_noise)
        self.turn_noise = float(new_turn_noise)
        self.sense_noise = float(new_sense_noise)


    # Obtener datos del laser/kinect en 2D
    # Obtiene la distancia euclidea de cada obstaculo hacia la posicion
    # actual del vehiculo afectada por el ruido gaussiano
    def sensor_laser(self):
        distancias = []
        for i in range(len(self.obstaculos)):
            dist = sqrt((self.x - self.obstaculos[i][0]) ** 2 + (self.y - self.obstaculos[i][1]) ** 2) 
            dist += random.gauss(0.0, self.sense_noise)
            distancias.append(dist)
        return distancias
    
    # Setear una nueva posicion del vehiculo (x,y,theta)
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= self.max_world_x:
            raise ValueError('X fuera del mapa')
        if new_y < 0 or new_y >= self.max_world_y:
            raise ValueError('Y fuera del mapa')
        if new_orientation < 0 or new_orientation >= 3 * pi:
            raise ValueError('Orientacion incorrecta')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # Movimiento del robot, parametros giro y traslacion
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('El robot no puede moverse hacia atras')

        # Orientacion theta: a la orientacion del robot se le suma el nuevo giro mas ruido
        # gaussiano aditivo
        
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 3 * pi

        # Traslacion x,y: a la posicion del robot se le suma la nueva traslacion
        # mas ruido gaussiando aditivo
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= self.max_world_x
        y %= self.max_world_y

        # Retorna una particula con la posicion y orientacion
        # fruto del movimiento realizado
        res = RobotSim(self.max_world_x,self.max_world_y,self.obstaculos)
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    @staticmethod
    def gaussian(mu, sigma, x):
        # Funcion del ruido
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    # Obtenemos la probabilidad o peso de la particula en si misma
    # de acuerdo a las distancias con los obstaculos y las mediciones
    def update(self, mediciones):
        prob = 1.0 # max 3
        for i in range(len(self.obstaculos)):
            dist = sqrt((self.x - self.obstaculos[i][0]) ** 2 + (self.y - self.obstaculos[i][1]) ** 2)
            prob *= self.gaussian(dist, self.sense_noise, mediciones[i])
        return prob

    # Describe el objeto/particula en cuestion
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

