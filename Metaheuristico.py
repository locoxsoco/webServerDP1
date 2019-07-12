import math
import random
import sys
# import time
import numpy
import Clases
import Main
from copy import deepcopy
from datetime import datetime,date, timedelta
from io import StringIO

class Annealer(object):
    # parámetros
    Tmax = 25000.0
    Tmin = 2.5
    steps = 5000

    max_accepts = 50
    max_improve = 20
    reheat =1.25
    max_iter = 100
    listaTabu = []

    def __init__(self,x,y,z):
        """
        Método FIFO para alcanzar una solución mas o menos óptima
        """
        self.listaVuelos = deepcopy(x)
        self.listaAreas = y+z

        for vuelo in self.listaVuelos:
            asignado = False
            for puertaZona in (self.listaAreas):
                if (puertaZona.insertarVuelo(vuelo,vuelo.tiempoEstimado)!=-1):
                    asignado = True
                    break
                    
            while(not asignado):
                vuelo.setTiempoLlegada (vuelo.tiempoLlegada + timedelta(minutes = 1))                
                for puertaZona in (self.listaAreas):
                    if (puertaZona.insertarVuelo(vuelo,vuelo.tiempoLlegada)!=-1):
                        asignado = True                        
                        break

        # sys.stdout = sys.__stdout__
        # for i in range(len(self.listaAreas)):
        #     if(i!=0):
        #         print (",", end="")
        #     self.listaAreas[i].imprimirLista()
        self.state = deepcopy(self.listaAreas)

    def move(self,tabu = False): 
        selector =round(random.random()) #round(random.random())
        if(selector == 0):
            #asignacion vuelo
            indiceArea = round(random.random()*(len(self.state)-1))

            if(self.state[indiceArea].vuelos.cantidad == 0):
                return 0
            numVuelo = round(random.random()*(self.state[indiceArea].vuelos.cantidad-1))+1
            #Tabu
            if (tabu):
                if(("Insert", self.state[indiceArea].idArea, self.state[indiceArea].tipoArea, numVuelo) in self.listaTabu):
                    return 0
                else: 
                    self.listaTabu.append(("Insert", self.state[indiceArea].idArea, self.state[indiceArea].tipoArea, numVuelo))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            cont = 0
            for p in range(len(self.state[indiceArea].vuelos.listaVuelos)):
                if (self.state[indiceArea].vuelos.listaVuelos[p].ocupado):
                    cont +=1
                    if (cont == numVuelo):
                        break

            # JSON antiguo            
            # print (self.state[indiceArea].tipoArea,self.state[indiceArea].idArea," - ",cont," ",numVuelo," ", self.state[indiceArea].vuelos.cantidad," ",cont<=self.state[indiceArea].vuelos.cantidad," ",self.state[indiceArea].vuelos.listaVuelos[p].tiempoInicio,"-",self.state[indiceArea].vuelos.listaVuelos[p].tiempoFin)
            if (self.state[indiceArea].vuelos.listaVuelos[p].vuelo.llego is True):
                return 0
            
            save = self.state[indiceArea].vuelos.listaVuelos[p].vuelo.tiempoLlegada
            self.state[indiceArea].vuelos.listaVuelos[p].vuelo.setTiempoLlegada (self.state[indiceArea].vuelos.listaVuelos[p].vuelo.tiempoEstimado)
            for puertaZona in range(len(self.state)):
                if (self.state[puertaZona]!= self.state[indiceArea] and \
                    self.state[puertaZona].insertarVuelo(self.state[indiceArea].vuelos.listaVuelos[p].vuelo,self.state[indiceArea].vuelos.listaVuelos[p].vuelo.tiempoEstimado)!=-1):
                    self.state[indiceArea].removeVuelo(self.state[indiceArea].vuelos.listaVuelos[p])
                    # print ("1",self.state[indiceArea].tipoArea,self.state[indiceArea].idArea," - ",self.state[indiceArea].vuelos.cantidad, " ", self.state[puertaZona].tipoArea,self.state[puertaZona].idArea," - ",self.state[puertaZona].vuelos.cantidad)
                    
                    return 1
            iter2 = 0 
            while (iter2 < 60 ):
                self.state[indiceArea].vuelos.listaVuelos[p].vuelo.setTiempoLlegada (self.state[indiceArea].vuelos.listaVuelos[p].vuelo.tiempoLlegada + timedelta(minutes = 1))
                for puertaZona in range(len(self.state)):
                    if (self.state[puertaZona]!= self.state[indiceArea] and \
                        self.state[puertaZona].insertarVuelo(self.state[indiceArea].vuelos.listaVuelos[p].vuelo,self.state[indiceArea].vuelos.listaVuelos[p].vuelo.tiempoLlegada)!=-1):
                        self.state[indiceArea].removeVuelo(self.state[indiceArea].vuelos.listaVuelos[p])
                        # print ("2",self.state[indiceArea].tipoArea,self.state[indiceArea].idArea," - ",self.state[indiceArea].vuelos.cantidad, " ", self.state[puertaZona].tipoArea,self.state[puertaZona].idArea," - ",self.state[puertaZona].vuelos.cantidad)
                        
                        return 1
                iter2 +=1
            self.state[indiceArea].vuelos.listaVuelos[p].vuelo.setTiempoLlegada(save)
            return 0
        else:
            #intercambio de intervalos
            indiceArea = round(random.random()*(len(self.state)-1))

            if(self.state[indiceArea].vuelos.cantidad == 0):
                return 0
            numVuelo = round(random.random()*(self.state[indiceArea].vuelos.cantidad-1))+1
            
            cont = 0
            for p in range(len(self.state[indiceArea].vuelos.listaVuelos)):
                if (self.state[indiceArea].vuelos.listaVuelos[p].ocupado):
                    cont +=1
                    if (cont == numVuelo):
                        break

            indiceArea2 = round(random.random()*(len(self.state)-1))
            if(indiceArea2 == indiceArea): 
                return 0
            if(self.state[indiceArea2].vuelos.cantidad == 0 or self.state[indiceArea].indice != self.state[indiceArea2].indice):
                return 0
            #Tabu
            if (tabu):
                if(("Exchange", self.state[indiceArea].idArea, numVuelo, self.state[indiceArea2].idArea) in self.listaTabu):
                    return 0
                else:
                    self.listaTabu.append(("Exchange", self.state[indiceArea].idArea, numVuelo, self.state[indiceArea2].idArea))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            encontro = False
            for p2 in range(len(self.state[indiceArea2].vuelos.listaVuelos)):
                if (self.state[indiceArea2].vuelos.listaVuelos[p2].ocupado):
                    if ((self.state[indiceArea2].vuelos.listaVuelos[p2].tiempoInicio <= self.state[indiceArea].vuelos.listaVuelos[p].tiempoFin and self.state[indiceArea2].vuelos.listaVuelos[p2].tiempoInicio >= self.state[indiceArea].vuelos.listaVuelos[p].tiempoInicio) \
                        # or (p2.tiempoFin <= p.tiempoFin and p2.tiempoFin >= p.tiempoInicio) \ 
                        or (self.state[indiceArea].vuelos.listaVuelos[p].tiempoInicio <= self.state[indiceArea2].vuelos.listaVuelos[p2].tiempoFin and self.state[indiceArea].vuelos.listaVuelos[p].tiempoInicio >= self.state[indiceArea2].vuelos.listaVuelos[p2].tiempoInicio)): 
                        # or (p.tiempoFin < p2.tiempoFin and p.tiempoFin > p2.tiempoInicio)):
                        encontro = True
                        break
            
            if (not encontro):
                return 0
            
            # JSON antiguo
            if (self.state[indiceArea].vuelos.listaVuelos[p].vuelo.llego is True or self.state[indiceArea2].vuelos.listaVuelos[p2].vuelo.llego is True):
                return 0
            A = Clases.Intervalo (self.state[indiceArea].vuelos.listaVuelos,self.state[indiceArea].vuelos.listaVuelos[p])
            B = Clases.Intervalo (self.state[indiceArea2].vuelos.listaVuelos,self.state[indiceArea2].vuelos.listaVuelos[p2])
            
            while not ((A.t2 >= B.t1 and A.t3 <= B.t4) and (B.t2 >= A.t1 and B.t3 <= A.t4)):    
                if (A.t2 < B.t1):
                    if (not B.extendLeft()):
                        return 0
                if (B.t2 < A.t1):
                    if (not A.extendLeft()):
                        return 0
                if (A.t3>B.t4): 
                    if (not B.extendRight()):
                        return 0
                if (B.t3>A.t4):
                    if (not A.extendRight()):
                        return 0

            for punt in range(A.listaVuelos.index(A.inicio),A.listaVuelos.index(A.fin)+1):
                if (A.listaVuelos[punt].ocupado):
                    self.state[indiceArea].removeVuelo(A.listaVuelos[punt])

                    A.listaVuelos[punt].vuelo.setTiempoLlegada (A.listaVuelos[punt].vuelo.tiempoEstimado)
                    while (True): 
                        if (self.state[indiceArea2].insertarVuelo(A.listaVuelos[punt].vuelo,A.listaVuelos[punt].vuelo.tiempoLlegada)!=-1):
                            break
                        A.listaVuelos[punt].vuelo.setTiempoLlegada (A.listaVuelos[punt].vuelo.tiempoLlegada + timedelta(minutes = 1))
                  
            for punt in range(B.listaVuelos.index(B.inicio),B.listaVuelos.index(B.fin)+1):
                if(B.listaVuelos[punt].ocupado):
                    self.state[indiceArea2].removeVuelo(B.listaVuelos[punt])
                    B.listaVuelos[punt].vuelo.setTiempoLlegada (B.listaVuelos[punt].vuelo.tiempoEstimado)
                    while (True): 
                        if (self.state[indiceArea].insertarVuelo(B.listaVuelos[punt].vuelo,B.listaVuelos[punt].vuelo.tiempoLlegada)!=-1):
                            break
                        B.listaVuelos[punt].vuelo.setTiempoLlegada (B.listaVuelos[punt].vuelo.tiempoLlegada + timedelta(minutes = 1))
        
            # print(l,end=" ")
            # l=0
            # for punt in range(A.listaVuelos.index(A.inicio),A.listaVuelos.index(A.fin)+1):
            #     if (A.listaVuelos[punt].ocupado):
            #         A.listaVuelos[punt].vuelo.setTiempoLlegada (A.listaVuelos[punt].vuelo.tiempoEstimado)
            #         while (True): 
            #             if (self.state[indiceArea2].insertarVuelo(A.listaVuelos[punt].vuelo,A.listaVuelos[punt].vuelo.tiempoLlegada)!=-1):
            #                 self.c+=1
            #                 l+=1
            #                 break
            #             A.listaVuelos[punt].vuelo.setTiempoLlegada (A.listaVuelos[punt].vuelo.tiempoLlegada + timedelta(minutes = 1))
                  
            # print(l,end=" ")  
            # l=0    
            # for punt in range(B.listaVuelos.index(B.inicio),B.listaVuelos.index(B.fin)+1):
            #     if(B.listaVuelos[punt].ocupado):
            #         B.listaVuelos[punt].vuelo.setTiempoLlegada (B.listaVuelos[punt].vuelo.tiempoEstimado)
            #         while (True): 
            #             if (self.state[indiceArea].insertarVuelo(B.listaVuelos[punt].vuelo,B.listaVuelos[punt].vuelo.tiempoLlegada)!=-1):
            #                 self.d+=1
            #                 l+=1
            #                 break
            #             B.listaVuelos[punt].vuelo.setTiempoLlegada (B.listaVuelos[punt].vuelo.tiempoLlegada + timedelta(minutes = 1))
            # print(l)
            return 1

    def energy(self,fin=True):
        """Calculate state's energy"""
        costoVuelos = 0
        costoTamano = 0
        parCastigo = 900000
        costoAreas = 0
        for puerta in self.state:
            costoAreas =0
            for p in puerta.vuelos.listaVuelos:
            # p = puerta.vuelos.inicio
            # while (p is not None):
                if (p.ocupado):
                    costoVuelos += (p.vuelo.tiempoLlegada - p.vuelo.tiempoEstimado).total_seconds() ** 2
                    costoTamano += (p.vuelo.area.indice - p.vuelo.avion.tipoAvion.indice)
                else:
                    if (puerta.tipoArea=="Manga"):
                        costoAreas += parCastigo * (p.tiempoFin - p.tiempoInicio).total_seconds()
                    else:
                        costoAreas += (p.tiempoFin - p.tiempoInicio).total_seconds()
                # p = p.sig
        
        return costoAreas + costoVuelos * 90000000 + costoTamano * 90000


    def anneal(self):
        """
        Minimizar el tiempo de espera de todos los vuelos ya asignados (tiempo real - tiempo programado) 
        y el tiempo sin usar de las puertas del aeropuerto.
        Parametros
        state : estado actual del recocido
        Retorna
        (state, energy): best state and energy found.
        """
        step = 0
        if self.Tmin <= 0.0:
            raise Exception('Exponential cooling requires a minimum "\
                "temperature greater than zero.')
        Tfactor = -math.log(self.Tmax / self.Tmin)

        T = self.Tmax
        E = self.energy(False)
        prevState = best_state= deepcopy(self.state)
        prevEnergy = best_energy = E
        trials, accepts, improves = 0, 0, 0
        unaccepts, unimproves = 0,0

        # Attempt moves to new states
        while step < self.steps:
            step += 1
            T = self.Tmax * math.exp(Tfactor * step / self.steps)
            if (self.move() == 0):
                # step -=1
                continue
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
        return best_state, best_energy