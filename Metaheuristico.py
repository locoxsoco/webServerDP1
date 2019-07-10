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
        selector =0 #round(random.random())
        if(selector == 0):
            #asignacion vuelo
            indiceArea = round(random.random()*(len(self.state)-1))
            area = (self.state)[indiceArea]

            if(area.vuelos.cantidad == 0):
                return 0
            numVuelo = round(random.random()*(area.vuelos.cantidad-1))+1
            # p = area.vuelos.inicio    
            #Tabu
            if (tabu):
                if(("Insert", area.idArea, area.tipoArea, numVuelo) in self.listaTabu):
                    return 0
                else: 
                    self.listaTabu.append(("Insert", area.idArea, area.tipoArea, numVuelo))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            cont = 0
            for p in range(len(area.vuelos.listaVuelos)):
            # while(p is not None):
                if (area.vuelos.listaVuelos[p].ocupado):
                    cont +=1
                    if (cont == numVuelo):
                        break

            # JSON antiguo            
            print (area.tipoArea,area.idArea," - ",cont," ",numVuelo," ", area.vuelos.cantidad," ",cont<=area.vuelos.cantidad," ",area.vuelos.listaVuelos[p].tiempoInicio,"-",area.vuelos.listaVuelos[p].tiempoFin)
            if (area.vuelos.listaVuelos[p].vuelo.llego is True):
                return 0
            
            save = deepcopy(area.vuelos.listaVuelos[p].vuelo.tiempoLlegada)
            area.vuelos.listaVuelos[p].vuelo.setTiempoLlegada (area.vuelos.listaVuelos[p].vuelo.tiempoEstimado)
            for puertaZona in range(len(self.state)):
                if (self.state[puertaZona]!= area and \
                    self.state[puertaZona].insertarVuelo(area.vuelos.listaVuelos[p].vuelo,area.vuelos.listaVuelos[p].vuelo.tiempoEstimado)!=-1):
                    area.removeVuelo(area.vuelos.listaVuelos[p])
                    print ("1",area.tipoArea,area.idArea," - ",area.vuelos.cantidad, " ", self.state[puertaZona].tipoArea,self.state[puertaZona].idArea," - ",self.state[puertaZona].vuelos.cantidad)
                    # print("Mover - 1",p.vuelo.numeroVuelo)
                    # area.imprimirLista()
                    # print()
                    # print ("area reemplazante")
                    # puertaZona.imprimirLista()
                    return 1
            iter2 = 0 
            while (iter2 < 60 ): 
                area.vuelos.listaVuelos[p].vuelo.setTiempoLlegada (area.vuelos.listaVuelos[p].vuelo.tiempoLlegada + timedelta(minutes = 1))
                for puertaZona in range(len(self.state)):
                    if (self.state[puertaZona]!= area and \
                        self.state[puertaZona].insertarVuelo(area.vuelos.listaVuelos[p].vuelo,area.vuelos.listaVuelos[p].vuelo.tiempoLlegada)!=-1):
                        area.removeVuelo(area.vuelos.listaVuelos[p])
                        print ("2",area.tipoArea,area.idArea," - ",area.vuelos.cantidad, " ", self.state[puertaZona].tipoArea,self.state[puertaZona].idArea," - ",self.state[puertaZona].vuelos.cantidad)
                        # print("Mover - 2",p.vuelo.numeroVuelo)
                        # area.imprimirLista()
                        # print()
                        # print ("area reemplazante")
                        # puertaZona.imprimirLista()
                        return 1
                iter2 +=1
            area.vuelos.listaVuelos[p].vuelo.setTiempoLlegada(save)
            return 0
        else:
            #intercambio de intervalos
            indiceArea = round(random.random()*(len(self.state)-1))
            area = (self.state)[indiceArea]

            if(area.vuelos.cantidad == 0):
                return 0
            numVuelo = round(random.random()*(area.vuelos.cantidad-1))+1
            
            cont = 0
            for p in range(len(area.vuelos.listaVuelos)):
            # while(p is not None):
                if (area.vuelos.listaVuelos[p].ocupado):
                    cont +=1
                    if (cont == numVuelo):
                        break

            indiceArea2 = round(random.random()*(len(self.state)-1))
            if(indiceArea2 == indiceArea): 
                return 0
            area2 = (self.state)[indiceArea2]
            if(area2.vuelos.cantidad == 0 or area.indice != area2.indice):
                return 0
            #Tabu
            if (tabu):
                if(("Exchange", area.idArea, numVuelo, area2.idArea) in self.listaTabu):
                    return 0
                else:
                    self.listaTabu.append(("Exchange", area.idArea, numVuelo, area2.idArea))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            # p2 = area2.vuelos.inicio
            encontro = False
            for p2 in range(len(area2.vuelos.listaVuelos)):
            # while(p2 is not None):
                if (area2.vuelos.listaVuelos[p2].ocupado):
                    if ((area2.vuelos.listaVuelos[p2].tiempoInicio <= area.vuelos.listaVuelos[p].tiempoFin and area2.vuelos.listaVuelos[p2].tiempoInicio >= area.vuelos.listaVuelos[p].tiempoInicio) \
                        # or (p2.tiempoFin <= p.tiempoFin and p2.tiempoFin >= p.tiempoInicio) \ 
                        or (area.vuelos.listaVuelos[p].tiempoInicio <= area2.vuelos.listaVuelos[p2].tiempoFin and area.vuelos.listaVuelos[p].tiempoInicio >= area2.vuelos.listaVuelos[p2].tiempoInicio)): 
                        # or (p.tiempoFin < p2.tiempoFin and p.tiempoFin > p2.tiempoInicio)):
                        encontro = True
                        break
                # p2=p2.sig
            
            if (not encontro):
                return 0
            
            # JSON antiguo
            if (area.vuelos.listaVuelos[p].vuelo.llego is True or area2.vuelos.listaVuelos[p2].vuelo.llego is True):
                return 0

            A = Clases.Intervalo (area.vuelos.listaVuelos,area.vuelos.listaVuelos[p])
            B = Clases.Intervalo (area2.vuelos.listaVuelos,area2.vuelos.listaVuelos[p2])
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

            # punt = A.inicio
            for punt in range(A.listaVuelos.index(A.inicio),A.listaVuelos.index(A.fin)+1):
                # indice = A.listaVuelos.index(A.listaVuelos[punt])
                if (A.listaVuelos[punt].ocupado):
                    # area.vuelos.listaVuelos.pop(indice)
                    area.removeVuelo(A.listaVuelos[punt])

            for punt in range(B.listaVuelos.index(B.inicio),B.listaVuelos.index(B.fin)+1):
                # indice = B.listaVuelos.index(B.listaVuelos[punt])
                if(B.listaVuelos[punt].ocupado):
                    # area2.vuelos.listaVuelos.pop(indice)
                    area2.removeVuelo(B.listaVuelos[punt])

            for punt in range(A.listaVuelos.index(A.inicio),A.listaVuelos.index(A.fin)+1):
                # indice = A.listaVuelos.index(punt)
                if (punt.ocupado):
                    A.listaVuelos[punt].vuelo.setTiempoLlegada (A.listaVuelos[punt].vuelo.tiempoEstimado)
                    while (True): 
                        if (area2.insertarVuelo(A.listaVuelos[punt].vuelo,A.listaVuelos[punt].vuelo.tiempoLlegada)!=-1):
                            break
                        A.listaVuelos[punt].vuelo.setTiempoLlegada (A.listaVuelos[punt].vuelo.tiempoLlegada + timedelta(minutes = 1))
                        
            for punt in range(B.listaVuelos.index(B.inicio),B.listaVuelos.index(B.fin)+1):
                # indice = B.listaVuelos.index(punt)
                if(B.listaVuelos[punt].ocupado):
                    B.listaVuelos[punt].vuelo.setTiempoLlegada (B.listaVuelos[punt].vuelo.tiempoEstimado)
                    while (True): 
                        if (area.insertarVuelo(B.listaVuelos[punt].vuelo,B.listaVuelos[punt].vuelo.tiempoLlegada)!=-1):
                            break
                        B.listaVuelos[punt].vuelo.setTiempoLlegada (B.listaVuelos[punt].vuelo.tiempoLlegada + timedelta(minutes = 1))
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