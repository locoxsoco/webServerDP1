import math
import random
import sys
import time
import numpy
import Clases
from copy import deepcopy
from datetime import datetime,date,time, timedelta
from io import StringIO

import sys
class Annealer(object):
    # parámetros
    Tmax = 25000.0
    Tmin = 2.5
    steps = 4000

    max_accepts = 50
    max_improve = 20
    reheat =1.25
    max_iter = 100
    listaTabu = []

    def __init__(self,x,y,z):
        """
        Método FIFO para alcanzar una solución mas o menos óptima
        """

        #print ("Original: ")
        self.listaVuelos = deepcopy(x)
        self.listaPuertas = deepcopy(y)
        self.listaZonas = deepcopy(z)
        self.listaAreas = self.listaPuertas + self.listaZonas
        self.maxTiempo = self.listaVuelos[0].tiempoEstimado
        self.minTiempo = self.listaVuelos[0].tiempoEstimado

        j=0
        for vuelo in self.listaVuelos:
            asignado = False
            j+=1
            for puerta in self.listaPuertas:
                if (puerta.insertarVuelo(vuelo,vuelo.tiempoEstimado)!=-1):
                    asignado = True
                    break
            if (asignado):
                continue
            for zona in self.listaZonas:
                if (zona.insertarVuelo(vuelo,vuelo.tiempoEstimado)!=-1):
                    asignado = True
                    break
                    
            while(not asignado):
                vuelo.tiempoLlegada += timedelta(minutes = 1)
                
                for puerta in self.listaPuertas:
                    if (puerta.insertarVuelo(vuelo,vuelo.tiempoLlegada)!=-1):
                        asignado = True                        
                        break
                if (asignado):
                    asignado = True
                    break
                for zona in self.listaZonas:
                    if (zona.insertarVuelo(vuelo,vuelo.tiempoLlegada)!=-1):
                        asignado = True
                        break
        self.state = (self.listaPuertas, self.listaZonas,self.listaVuelos)
        best_state = deepcopy(self.state)
        best_energy = self.energy(False) #CAMBIAR PARA EXPNUM
        
        x= best_state
        y=best_energy

    def move(self,tabu = False):
        selector =round(random.random())
        if(selector == 0):
            #asignacion vuelo
            indiceArea = round(random.random()*(len(self.state[0]+self.state[1])-1))
            area = (self.state[0]+self.state[1])[indiceArea]

            if(area.vuelos.cantidad == 0):
                return
            indiceVuelo = round(random.random()*(area.vuelos.cantidad-1))+1
            cont = 1
            p = area.vuelos.inicio            
            #Tabu
            if (tabu):
                if(("Insert", area.idArea, indiceVuelo) in self.listaTabu):
                    return
                else: 
                    self.listaTabu.append(("Insert", area.idArea, indiceVuelo))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            while(p is not None):
                if (p.ocupado):
                    if (cont == indiceVuelo):
                        break
                    cont +=1                              
                p=p.sig


            p.vuelo.setTiempoLlegada (p.vuelo.tiempoEstimado)
            for puerta in self.state[0]:
                if (puerta != area and puerta.insertarVuelo(p.vuelo,p.vuelo.tiempoEstimado)!=-1):
                    area.removeVuelo(p)
                    return
            for zona in self.state[1]:
                if (zona != area and zona.insertarVuelo(p.vuelo,p.vuelo.tiempoEstimado)!=-1):
                    area.removeVuelo(p)
                    return
            iter2 = 1 
            while (True):
                p.vuelo.tiempoLlegada += timedelta(minutes = 1)
                for puerta in self.state[0]:
                    if (puerta.insertarVuelo(p.vuelo,p.vuelo.tiempoLlegada)!=-1):
                        area.removeVuelo(p)
                        return

                for zona in self.state[1]:
                    if (zona.insertarVuelo(p.vuelo,p.vuelo.tiempoLlegada)!=-1):
                        area.removeVuelo(p)
                        return 
                iter2 +=1
                if (iter2 > 60 ):
                    return
        else:
            #intercambio de intervalos
            indiceArea = round(random.random()*(len(self.state[0]+self.state[1])-1))
            area = (self.state[0]+self.state[1])[indiceArea]

            if(area.vuelos.cantidad == 0):
                return
            indiceVuelo = round(random.random()*(area.vuelos.cantidad-1))+1
            cont = 1
            p = area.vuelos.inicio
            while(p is not None):
                if (p.ocupado):
                    if (cont == indiceVuelo):
                        break
                    cont +=1                              
                p=p.sig

            
            indiceArea2 = round(random.random()*(len(self.state[0]+self.state[1])-1))
            if(indiceArea2 == indiceArea): 
                return
            area2 = (self.state[0]+self.state[1])[indiceArea2]
            if(area2.vuelos.cantidad == 0):
                return

            #Tabu
            if (tabu):
                if(("Exchange", area.idArea, indiceVuelo, area2.idArea) in self.listaTabu):
                    return
                else: 
                    self.listaTabu.append(("Exchange", area.idArea, indiceVuelo, area2.idArea))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])


            p2 = area2.vuelos.inicio
            while(p2 is not None):
                if (p2.ocupado):
                    if ((p2.tiempoInicio < p.tiempoFin and p2.tiempoInicio > p.tiempoInicio) or \
                        (p2.tiempoFin < p.tiempoFin and p2.tiempoFin > p.tiempoInicio) or \
                        (p.tiempoInicio < p2.tiempoFin and p.tiempoInicio > p2.tiempoInicio)or 
                        (p.tiempoFin < p2.tiempoFin and p.tiempoFin > p2.tiempoInicio)):
                        break
                p2=p2.sig
            if (p2 is None):
                return
            A = Clases.Intervalo (p)
            B = Clases.Intervalo (p2)
            while not ((A.t2 >= B.t1 and A.t3 <= B.t4) and \
                (B.t2 >= A.t1 and B.t3 <= A.t4)):    
                if (A.t2 < B.t1):
                    if (not B.extendLeft()):
                        return
                if (B.t2 < A.t1):
                    if (not A.extendLeft()):
                        return
                if (A.t3>B.t4):
                    if (not B.extendRight()):
                        return
                if (B.t3>A.t4):
                    if (not A.extendRight()):
                        return
            #area.exchange(area2, A, B) 

    def energy(self,fin=True):
        """Calculate state's energy"""
        #for i in (self.state[0]+self.state[1]):
        #    i.imprimirLista()
        for i in self.state[2]:
            if(self.maxTiempo < i.tiempoLlegada):
                self.maxTiempo = i.tiempoLlegada
            if(self.minTiempo > i.tiempoLlegada):
                self.minTiempo = i.tiempoLlegada
        # maxTiempo = self.maxTiempo + timedelta(hours=2)
        # minTiempo =self.minTiempo - timedelta(hours=1)

        costoVuelos = 0
        parCastigo = 900000
        xd=0
        for i in self.state[2]:
            costoVuelos += (i.tiempoLlegada - i.tiempoEstimado).total_seconds() ** 2
            xd += (i.tiempoLlegada - i.tiempoEstimado).total_seconds()
        if (fin):
            #print (self.maxTiempo, self.minTiempo)
            print ("Hora asignada y hora estimada (L) : "+ str(xd/3600))
        xd=0        
        costoAreas = 0
        for puerta in self.state[0]:
            costoPuerta =0
            c = 1
            p = puerta.vuelos.inicio
            #print ("Cantidad: " + str(puerta.vuelos.cantidad), end='')
            #print (" | Bloque: " + str(puerta.vuelos.cantBloques) + " de la puerta: "+ str(puerta.idArea))
            while (p is not None):
                if not(p.ocupado) and c != 1 and c != puerta.vuelos.cantBloques:
                    costoPuerta += (p.tiempoFin - p.tiempoInicio).total_seconds()
                p = p.sig
                c+=1
            costoAreas += parCastigo * costoPuerta
            xd +=costoPuerta
        
        if (fin):
            print("Tiempo sin uso de Puertas (P*U) : "+ str(xd/3600))
        xd=0
        for zona in self.state[1]:
            costoZona = 0
            c=1
            p = zona.vuelos.inicio
            while (p is not None):
                if not(p.ocupado) and c != 1 and c != zona.vuelos.cantBloques:
                    costoZona += (p.tiempoFin - p.tiempoInicio).total_seconds()
                p = p.sig
                c+=1 
            costoAreas += costoZona
            xd +=costoZona
        if (fin):
            print("Tiempo sin uso de Zonas (U) "+ str(xd/3600))
        return costoAreas + costoVuelos

    def anneal(self):
        """
        Minimizar el tiempo de espera de todos los vuelos ya asignados (tiempo real - tiempo programado) 
        y el tiempo sin usar de las puertas del aeropuerto.
        Parameters
        state : an initial arrangement of the system
        Returns
        (state, energy): the best state and energy found.
        """
        step = 0
        if self.Tmin <= 0.0:
            raise Exception('Exponential cooling requires a minimum "\
                "temperature greater than zero.')
        Tfactor = -math.log(self.Tmax / self.Tmin)

        T = self.Tmax
        E = self.energy(False)
        prevState = deepcopy(self.state)
        prevEnergy = E
        best_state = deepcopy(self.state)
        best_energy = E
        trials, accepts, improves = 0, 0, 0
        unaccepts, unimproves = 0,0

        # Attempt moves to new states
        while step < self.steps:
            step += 1
            T = self.Tmax * math.exp(Tfactor * step / self.steps)
            self.move()
            E = self.energy(False)
            dE = E - prevEnergy
            trials += 1
            if dE > 0.0 and math.exp(-dE / T) < random.random():
                # Restore previous state
                self.state = deepcopy(prevState)
                E = prevEnergy
                unaccepts += 1
            else:
                # Accept new state and compare to best state
                accepts += 1
                if dE < 0.0:
                    improves += 1
                else: 
                    unimproves +=1
                prevState = deepcopy(self.state)
                prevEnergy = E
                if E < best_energy:
                    best_state = deepcopy(self.state)
                    best_energy = E
            #Iterative Tabu Search        
            if (unaccepts > self.max_accepts or unimproves > self.max_improve):
                unaccepts = 0
                unimproves = 0
                iters =0
                while(iters <= self.max_iter):
                    self.move(True)
                    E = self.energy(False)
                    dE = E-prevEnergy
                    if dE < 0.0 :
                        prevState = deepcopy(self.state)
                        prevEnergy = E
                        if (E < best_energy):
                            best_state = deepcopy(self.state)
                            best_energy = E
                    iters+=1
                T = T * self.reheat
            if (T<= 0.001):
                break

        # Return best state and energy
        self.state = deepcopy(best_state)

        #print("Final: ") 
        self.energy(False) #CAMBIAR PARA EXPNUM
        return best_state, best_energy