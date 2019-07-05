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
        self.listaVuelos = (x)
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
                        
        self.state = (self.listaAreas,self.listaVuelos)
        # best_state = deepcopy(self.state)
        # best_energy = self.energy(False) #CAMBIAR PARA EXPNUM
        
        # x= best_state
        # y=best_energy

    def move(self,tabu = False):
        selector =round(random.random())
        if(selector == 0):
            #asignacion vuelo
            indiceArea = round(random.random()*(len(self.state[0])-1))
            area = (self.state[0])[indiceArea]

            if(area.vuelos.cantidad == 0):
                return 0
            indiceVuelo = round(random.random()*(area.vuelos.cantidad-1))+1
            p = area.vuelos.inicio    
            #Tabu
            if (tabu):
                if(("Insert", area.idArea, area.tipoArea, indiceVuelo) in self.listaTabu):
                    return 0
                else: 
                    self.listaTabu.append(("Insert", area.idArea, area.tipoArea, indiceVuelo))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            cont = 0
            while(p is not None):
                if (p.ocupado):
                    cont +=1
                    if (cont == indiceVuelo):
                        break
                p=p.sig
            # JSON antiguo
            if (p.vuelo.llego is True):
                return 0

            p.vuelo.setTiempoLlegada (p.vuelo.tiempoEstimado)
            for puertaZona in (self.state[0]):
                if (puertaZona.insertarVuelo(p.vuelo,p.vuelo.tiempoEstimado)!=-1):
                    area.removeVuelo(p)
                    return 1
            iter2 = 1 
            while (True): 
                p.vuelo.setTiempoLlegada (p.vuelo.tiempoLlegada + timedelta(minutes = 1))
                for puertaZona in (self.state[0]):
                    if (puertaZona.insertarVuelo(p.vuelo,p.vuelo.tiempoLlegada)!=-1):
                        area.removeVuelo(p)
                        # print("Mover - 2")
                        # area.imprimirLista()
                        # puertaZona.imprimirLista()
                        return 1

                iter2 +=1
                if (iter2 > 60):
                    p.vuelo.setTiempoLlegada(p.vuelo.tiempoEstimado)
                    return 0
        else:
            #intercambio de intervalos
            indiceArea = round(random.random()*(len(self.state[0])-1))
            area = (self.state[0])[indiceArea]

            if(area.vuelos.cantidad == 0):
                return 0
            indiceVuelo = round(random.random()*(area.vuelos.cantidad-1))+1
            cont = 0
            p = area.vuelos.inicio
            while(p is not None):
                if (p.ocupado):
                    cont +=1      
                    if (cont == indiceVuelo):
                        break                 
                p=p.sig

            indiceArea2 = round(random.random()*(len(self.state[0])-1))
            if(indiceArea2 == indiceArea): 
                return 0
            area2 = (self.state[0])[indiceArea2]
            if(area2.vuelos.cantidad == 0 or area.indice != area2.indice):
                return 0
            #Tabu
            if (tabu):
                if(("Exchange", area.idArea, indiceVuelo, area2.idArea) in self.listaTabu):
                    return 0
                else:
                    self.listaTabu.append(("Exchange", area.idArea, indiceVuelo, area2.idArea))
                    if (len(self.listaTabu)>50):
                        self.listaTabu.remove(self.listaTabu[0])

            p2 = area2.vuelos.inicio
            while(p2 is not None):
                if (p2.ocupado):
                    if ((p2.tiempoInicio < p.tiempoFin and p2.tiempoInicio > p.tiempoInicio) or (p2.tiempoFin < p.tiempoFin and p2.tiempoFin > p.tiempoInicio) or (p.tiempoInicio < p2.tiempoFin and p.tiempoInicio > p2.tiempoInicio) or (p.tiempoFin < p2.tiempoFin and p.tiempoFin > p2.tiempoInicio)):
                        break
                p2=p2.sig
            
            if (p2 is None):
                return 0
            
            # JSON antiguo
            if (p.vuelo.llego is True or p2.vuelo.llego is True):
                return 0

            A = Clases.Intervalo (p)
            B = Clases.Intervalo (p2)
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
            #intercambio
            copiaA = deepcopy(A)
            copiaB = deepcopy(B)

            punt = A.inicio
            while (True):
                if (punt.ocupado):
                    area.removeVuelo(punt)
                    #eliminar vuelo de la lista
                if(punt == A.fin):
                    break
                punt=punt.sig
            punt = B.inicio
            while(True):
                if(punt.ocupado):
                    area2.removeVuelo(punt)
                    #eliminar vuelo
                if(punt == B.fin):
                    break
                punt = punt.sig
            punt = copiaA.inicio
            while (True):
                if (punt.ocupado):
                    # Versión antigua
                    # area2.insertarVuelo(punt.vuelo,punt.vuelo.tiempoLlegada)
                    #Versión nueva
                    punt.vuelo.setTiempoLlegada (punt.vuelo.tiempoEstimado)
                    while (True): 
                        punt.vuelo.setTiempoLlegada (punt.vuelo.tiempoLlegada + timedelta(minutes = 1))
                        if (area2.insertarVuelo(punt.vuelo,punt.vuelo.tiempoLlegada)!=-1):
                            break
                    
                if(punt == copiaA.fin):
                    break
                punt=punt.sig
            punt = copiaB.inicio
            while (True):
                if (punt.ocupado):
                    # Versión antigua
                    #area.insertarVuelo(punt.vuelo,punt.vuelo.tiempoLlegada)
                    #Versión nueva
                    punt.vuelo.setTiempoLlegada (punt.vuelo.tiempoEstimado)
                    while (True): 
                        punt.vuelo.setTiempoLlegada (punt.vuelo.tiempoLlegada + timedelta(minutes = 1))
                        if (area.insertarVuelo(punt.vuelo,punt.vuelo.tiempoLlegada)!=-1):
                            break
                if(punt == copiaB.fin):
                    break
                punt=punt.sig
            return 1

    def energy(self,fin=True):
        """Calculate state's energy"""
        costoVuelos = 0
        costoTamano = 0
        parCastigo = 900000
        for i in self.state[1]:
            costoVuelos += (i.tiempoLlegada - i.tiempoEstimado).total_seconds() ** 2
            costoTamano += (i.area.indice - i.avion.tipoAvion.indice)
        '''    
            xd += (i.tiempoLlegada - i.tiempoEstimado).total_seconds()
        if (fin):
            #print (self.maxTiempo, self.minTiempo)
            print ("Hora asignada y hora estimada (L) : "+ str(xd/3600))
        xd=0        
        '''
        costoAreas = 0
        for puerta in self.state[0]:
            costoAreas =0
            c = 1
            p = puerta.vuelos.inicio
            #print ("Cantidad: " + str(puerta.vuelos.cantidad), end='')
            #print (" | Bloque: " + str(puerta.vuelos.cantBloques) + " de la puerta: "+ str(puerta.idArea))
            while (p is not None):
                if not(p.ocupado) and c != 1 and c != puerta.vuelos.cantBloques:
                    if (puerta.tipoArea=="Manga"):
                        costoAreas += parCastigo * (p.tiempoFin - p.tiempoInicio).total_seconds()
                    else:
                        costoAreas += (p.tiempoFin - p.tiempoInicio).total_seconds()
                p = p.sig
                c+=1
        
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
                step -=1
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

        # Return best state and energy
        #self.state = deepcopy(best_state)
        #print("Final: ") 
        #self.energy(False) #CAMBIAR PARA EXPNUM

        return best_state, best_energy