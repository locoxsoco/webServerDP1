from datetime import datetime, date,time, timedelta
from io import StringIO
from copy import deepcopy

import sys

class Avion :
    def __init__ (self,reg_number=None,icao=None,tipoAvion=None,tAerolinea=None):
        pass
    
    def addRegNumber (self,reg_number):
        self.regNumber = reg_number

    def addIata(self, iata):
        self.iata = iata

    def addIcao(self, icao):
        self.icao = icao

    def addTipoAvion(self, tipoAvion):
        self.tipoAvion = tipoAvion

    def addTAerolinea(self, tAerolinea):
        self.tAerolinea = tAerolinea

class Aeropuerto:
    def __init__ (self, iata=None, icao=None):
        pass

    def addIata(self, iata):
        self.iata = iata

    def addIcao(self, icao):
        self.icao = icao

class TAerolinea:
    def __init__ (self,idAerolinea=None, iata=None,icao=None):
        pass

    def addIdAerolinea(self, idAerolinea):
        self.idAerolinea = idAerolinea

    def addIata(self, iata):
        self.iata = iata

    def addIcao(self, icao):
        self.icao = icao

    def addNombre(self,nombre):
        self.nombre = nombre

class TipoAvion:
    def __init__(self,regNumber = None,capacidad = None,largo = None,ancho = None): 
        pass

    def addRegNumber (self,reg_number):
        self.regNumber = reg_number

    def addCapacidad(self,capacidad):
        self.capacidad = capacidad

    def addLargo(self,largo):
        self.largo = largo

    def addAncho(self,ancho):
        self.ancho=ancho

class Vuelo:    
    nVuelo = 0    
    def __init__ (self,  estado = None, avion =None,tiempoEstimado =None,tiempoProgramado=None, \
        tiempoLlegada=None,  icao=None, iata=None, \
        numeroVuelo=None,estaEnTierra=None,latitud=None,longitud=None, \
        altura=None, direccion=None, velocidadHorizontal=None, velocidadVertical=None,
        aeropuertoOrigen = None):
        self.asignado = False
        self.area=None
        self.estado=estado
        self.avion=avion
        self.tiempoEstimado=tiempoEstimado
        self.tiempoProgramado=tiempoProgramado
        self.tiempoLlegada=tiempoLlegada
        self.iata=iata
        self.icao=icao
        self.numeroVuelo=numeroVuelo
        self.estaEnTierra=estaEnTierra
        self.latitud=latitud
        self.longitud=longitud
        self.altura=altura
        self.direccion = direccion
        self.velocidadHorizontal = velocidadHorizontal
        self.velocidadVertical = velocidadVertical
        self.aeropuertoOrigen = aeropuertoOrigen
        self.idVuelo = 0

    def setEstado(self,estado):
        self.estado = estado

    def setAvion (self,avion):
        self.avion=avion

    def setTiempoEstimado (self,tiempoEstimado):
        self.tiempoEstimado = tiempoEstimado

    def addTiempoProgramado (self,tiempoProgramado):
        # no se usa, ahora todo será addTiempoEstimado
        self.tiempoProgramado=tiempoProgramado

    def setTiempoLlegada (self, tiempoLlegada):
        self.tiempoLlegada = tiempoLlegada

    def addIata(self, iata):
        self.iata = iata

    def addIcao(self, icao):
        self.icao = icao

    def addNumeroVuelo(self,numeroVuelo):
        self.numeroVuelo=numeroVuelo

    def addEstaEnTierra(self,estaEnTierra):
        self.estaEnTierra = estaEnTierra

    def addLatitud(self,latitud):
        self.latitud =latitud

    def addLongitud(self,longitud):
        self.longitud=longitud

    def addAltura(self,altura):
        self.altura=altura

    def addDireccion(self,direccion):
        self.direccion=direccion
        
    def addVelocidadHorizontal(self,velocidadHorizontal):
        self.velocidadHorizontal = velocidadHorizontal

    def addVelocidadVertical(self,velocidadVertical):
        self.velocidadVertical = velocidadVertical 

    def addAeropuertoOrigen(self,aeropuertoOrigen):
        self.aeropuertoOrigen = aeropuertoOrigen 

    def asignarPuerta (self, flagArea, area): 
        self.flagArea = flagArea # 1: zona, 0: puerta
        self.area = area # puntero a puerta o zona
        self.asignado=True

    def asignarIDVuelo(self):
        Vuelo.nVuelo +=1
        self.idVuelo = Vuelo.nVuelo

    def printData(self):
        #print("Numero de vuelo: " + str(self.numeroVuelo)+ " | ", end='')
        #if (self.area is not None):
        #    print("Puerta: " + str(self.area.idArea)+ " | ", end='')
        #print("tiempoEstimado: " + str(self.tiempoEstimado) +" | tiempoLlegada: " + str(self.tiempoLlegada) )
        pass

class BloqueVuelo:
    def __init__(self):
        self.vuelo = None
        self.ocupado=None
        self.tiempoInicio = None
        self.tiempoFin = None
        self.sig = None
        self.ant = None

    def addVuelo(self,vuelo,tiempo):
        self.vuelo = vuelo
        self.ocupado = True
        t=tiempo

        self.tiempoInicio = t-timedelta(hours =1)
        self.tiempoFin = t + timedelta(hours=2)

    def definirEspacioVacio(self, tiempoInicio, tiempoFin):
        self.tiempoInicio = tiempoInicio
        self.tiempoFin=tiempoFin
        self.ocupado=False

class ListaVuelos:
    def __init__ (self):
        self.inicio = BloqueVuelo()

        dia = datetime.now()
        self.tiempoInicio= datetime(year=2019,month =1,day=1,\
            hour=0,minute=0,second=0)
        self.tiempoFin= datetime(year=2020,month =1,day=1,\
            hour=0,minute=0,second=0)

        self.inicio.definirEspacioVacio(self.tiempoInicio,self.tiempoFin)
        self.fin = self.inicio
        self.cantidad=0
        self.cantBloques=1
        #self.tiempoLibre = self.tiempoFin - self.tiempoInicio
        
    def insertarBloque (self, bloque,pos=0):
        p = self.inicio
        ant = None
        ubicado = False
        while(p is not None):
            if (not p.ocupado and p.tiempoInicio <= bloque.tiempoInicio and \
                p.tiempoFin >= bloque.tiempoFin):

                #self.tiempoLibre = self.tiempoLibre - (bloque.tiempoFin - bloque.tiempoInicio)
                bloqueAnt = ant    
                bloqueSig = p.sig
                if (p.tiempoInicio != bloque.tiempoInicio):
                    bloqueAnt = BloqueVuelo()
                    bloqueAnt.definirEspacioVacio(p.tiempoInicio,bloque.tiempoInicio)
                    if(ant is None):
                        self.inicio = bloqueAnt
                    else:
                        ant.sig = bloqueAnt
                        bloqueAnt.ant = ant #doblemente enlazado 
                    self.cantBloques += 1
                if (p.tiempoFin != bloque.tiempoFin):
                    bloqueSig = BloqueVuelo()
                    bloqueSig.definirEspacioVacio(bloque.tiempoFin,p.tiempoFin)
                    bloqueSig.sig = p.sig
                    bloqueSig.ant = p #doblemente enlazado 
                    self.cantBloques += 1

                if(bloqueAnt is None):
                    self.inicio = bloque
                else:
                    bloqueAnt.sig = bloque

                if(bloqueSig is not None):
                    bloqueSig.ant = bloque #doblemente enlazado

                bloque.sig = bloqueSig
                bloque.ant = bloqueAnt
                self.cantidad +=1
                ubicado = True
                break
            ant = p
            p = p.sig
        if (ubicado): 
            return 1 #self.tiempoLibre
        else: 
            return -1

class Area:
    def __init__ (self, idArea=0, largo=0.0, ancho=0.0, coordenadaXCentro=0.0, \
        coordenadaYCentro=0.0):
        self.idArea = idArea
        self.largo = largo
        self.ancho = ancho
        self.vuelos = ListaVuelos()
        #self.tiempoLibre = self.vuelos.tiempoLibre


    def imprimirLista(self):
        if(self.idArea % 2 ==0):
            print ("{ \"tipo\": \""+ "puerta "+str(self.idArea//2) + "\", ",end="")
        else:
            print ("{ \"tipo\": \""+ "zona "+str(self.idArea//2 + 1) + "\", ", end ="")
        print ("\"vuelos\": [ ",end="")
        p=self.vuelos.inicio
        f = 0
        while(p is not None):
            if (p.ocupado):
                if (f==0):
                    f=1
                else:
                    print(", ",end="")
            #if (p.ocupado):
                print("{ \"numeroVuelo\": \""+ str(p.vuelo.icao) \
                    + "\", \"TiempoEstimado\": \""+ str(p.vuelo.tiempoEstimado) \
                    + "\", \"TiempoLlegada\": \""+ str(p.vuelo.tiempoLlegada) + "\" }",end="") 
            #else:
            #    print("{ \"TiempoINI\": \""+ str(p.tiempoInicio) \
            #        + "\", \"TiempoFIN\": \""+ str(p.tiempoFin) + "\" }",end="") 
            p=p.sig            
        print(" ] }",end="")
        #print("-------------------------------")

    def removeVuelo(self,bloque):
        p = self.vuelos.inicio
        ant = None
        while (p is not None):
            if(p == bloque):
                if(ant is not None and p.sig is not None):
                    if (not ant.ocupado and not p.sig.ocupado):
                        ant.definirEspacioVacio(ant.tiempoInicio, p.sig.tiempoFin)
                        ant.sig = p.sig.sig 
                        if(p.sig.sig is not None):
                            p.sig.sig.ant = ant #doblemente enlazado
                        
                        self.vuelos.cantBloques -= 1
                    elif (not ant.ocupado):
                        ant.definirEspacioVacio(ant.tiempoInicio,p.tiempoFin)
                        ant.sig = p.sig 
                        p.sig.ant = ant #doblemente enlazado
                    elif (not p.sig.ocupado):
                        p.sig.definirEspacioVacio(p.tiempoInicio,p.sig.tiempoFin)
                        ant.sig = p.sig
                        p.sig.ant = ant #doblemente enlazado
                    else:
                        bloqueVacio = BloqueVuelo()
                        bloqueVacio.definirEspacioVacio(p.tiempoInicio, p.tiempoFin)
                        self.vuelos.cantBloques += 1
                        ant.sig = bloqueVacio
                        bloqueVacio.sig = p.sig
                        bloqueVacio.ant = ant #doblemente enlazado
                        p.sig.ant = bloqueVacio #doblemente enlazado

                elif (ant is None):
                    if not(p.sig.ocupado):
                        p.sig.definirEspacioVacio(p.tiempoInicio, p.sig.tiempoFin)
                        self.vuelos.inicio = p.sig
                    else:
                        bloqueVacio = BloqueVuelo()
                        bloqueVacio.definirEspacioVacio(p.tiempoInicio, p.tiempoFin)
                        bloqueVacio.sig = p.sig
                        p.sig.ant = bloqueVacio #doblemente enlazado
                        self.vuelos.inicio = bloqueVacio
                        self.vuelos.cantBloques += 1
                elif(p.sig is None):
                    if(not ant.ocupado):
                        ant.sig = None
                        ant.definirEspacioVacio(ant.tiempoInicio, p.tiempoFin)
                    else:
                        bloqueVacio = BloqueVuelo()
                        bloqueVacio.definirEspacioVacio(p.tiempoInicio, p.tiempoFin)
                        ant.sig = bloqueVacio
                        bloqueVacio.ant = ant #doblemente enlazado

                self.vuelos.cantBloques -=1
                self.vuelos.cantidad -=1
                break
            ant = p
            p=p.sig

    def exchange(self, area, A, B):
        C = deepcopy (A)
        D = deepcopy (B)
        self.vuelos.cantidad -= B.cantidad
        self.vuelos.cantidad += A.cantidad
        area.vuelos.cantidad -= A.cantidad
        area.vuelos.cantidad += B.cantidad
        insertarIntervalo(self, C, D)
        C = deepcopy (A)
        D = deepcopy (B)
        insertarIntervalo(area, D, C)
        
############################################################################

class Zona(Area):
    def __init__ (self, idArea=0, largo=0.0, ancho=0.0, coordenadaXCentro=0.0, \
        coordenadaYCentro=0):
        Area.__init__(self, idArea, largo,ancho,coordenadaXCentro, coordenadaYCentro)

    def insertarVuelo(self, vuelo,tiempo):
        bloque = BloqueVuelo()
        bloque.addVuelo(vuelo,tiempo)
        insercion = self.vuelos.insertarBloque(bloque)
        if (insercion != -1 ):
            bloque.vuelo.asignarPuerta (1, self)
            return 1
        else:
            return -1

class Puerta(Area):
    def __init__ (self, idArea=0, largo=0.0, ancho=0.0, coordenadaXCentro=0.0, \
        coordenadaYCentro=0.0, velocidadDesembarco = 0.0):
        Area.__init__(self, idArea, largo,ancho, coordenadaXCentro, coordenadaYCentro)
        self.velocidadDesembarco = velocidadDesembarco

    def insertarVuelo(self, vuelo,tiempo):
        bloque = BloqueVuelo()        
        bloque.addVuelo(vuelo,tiempo)
        insercion = self.vuelos.insertarBloque(bloque)
        if (insercion != -1 ):
            bloque.vuelo.asignarPuerta (0, self)
            return 1
        else:
            return -1

class Manga: 
    def __init__(self):
        pass

    def asignarPuerta(self, puerta):
        self.puerta=puerta

class Intervalo(object):
    def __init__(self, bloque):
        if (bloque.ant is not None and not bloque.ant.ocupado):
            self.inicio = bloque.ant
            self.t1 = bloque.ant.tiempoInicio
        else:
            self.inicio = bloque
            self.t1 = bloque.tiempoInicio

        self.t2 = bloque.tiempoInicio
        self.t3 = bloque.tiempoFin

        if(bloque.sig is not None and not bloque.sig.ocupado):
            self.fin = bloque.sig
            self.t4 = bloque.sig.tiempoFin
        else:
            self.fin = bloque
            self.t4 = bloque.tiempoFin

        self.cantidad = 1

    def printIntervalo(self):
        p=self.inicio
        while (True):
            print (" => "+ str(p.tiempoInicio) + " | "+ str(p.tiempoFin),end="") 
            if(p == self.fin):
                break
            p=p.sig
        print ()
        print(str(self.t1),end=" ")
        print(str(self.t2),end=" ")
        print(str(self.t3),end=" ")
        print(self.t4)

    def extendLeft(self):
        if (self.inicio.ant is None):
            return False
        else:
            self.inicio = self.inicio.ant
            self.t2 = self.inicio.tiempoInicio

            if (self.inicio.ant is not None and not self.inicio.ant.ocupado):
                self.inicio = self.inicio.ant
            self.t1 = self.inicio.tiempoInicio

            self.cantidad +=1
            return True

    def extendRight(self):
        if (self.fin.sig is None):
            return False
        else:
            self.fin=self.fin.sig
            self.t3 = self.fin.tiempoFin

            if(self.fin.sig is not None and not self.fin.sig.ocupado):
                self.fin = self.fin.sig
            self.t4 = self.fin.tiempoFin
            
            self.cantidad +=1
            return True
        

def insertarIntervalo(area1, A, B):
    if (A.inicio.ant is None):
        if (B.t1==B.t2):
            area1.vuelos.inicio.definirEspacioVacio( \
                area1.vuelos.inicio.tiempoInicio, B.t1)
            B.inicio.ant = area1.vuelos.inicio
            area1.vuelos.inicio.sig = B.inicio
        else: 
            area1.vuelos.inicio.definirEspacioVacio( \
                area1.vuelos.inicio.tiempoInicio, B.t2)
            B.inicio.sig.ant = area1.vuelos.inicio
            area1.vuelos.inicio.sig = B.inicio.sig
    else:
        if (B.t1==B.t2):
            if (A.t1 < B.t1):
                bloqueVacio = BloqueVuelo()
                bloqueVacio.definirEspacioVacio(A.t1, B.t1)
                area1.vuelos.cantBloques += 1
                A.inicio.ant.sig = bloqueVacio
                bloqueVacio.ant = A.inicio.ant
                bloqueVacio.sig = B.inicio
                B.inicio.ant = bloqueVacio
            else:
                A.inicio.ant.sig = B.inicio
                #cantBloques
                B.inicio.ant = A.inicio.ant
        else:
            if(A.t1 < B.t1):
                B.inicio.definirEspacioVacio(A.t1, B.t2)
                area1.vuelos.cantBloques += 1
                A.inicio.ant.sig = B.inicio
                B.inicio.ant = A.inicio.ant
            else:
                A.inicio.ant.sig = B.inicio.sig
                #cantBloques
                B.inicio.ant = A.inicio.ant
        

    if (A.fin.sig is None):
        if(B.t3 == B.t4):
            A.fin.definirEspacioVacio(B.t4, A.fin.tiempoFin)
            B.fin.sig = A.fin
            A.fin.ant = B.fin
        else:
            A.fin.definirEspacioVacio(B.t3, A.fin.tiempoFin)
            B.fin.ant.sig = A.fin
            A.fin.ant = B.fin.ant
    else:
        if(B.t3 == B.t4):
            if(A.t4 < B.t4):
                bloqueVacio = BloqueVuelo()
                bloqueVacio.definirEspacioVacio(A.t4, B.t4)
                area1.vuelos.cantBloques+=1
                A.fin.sig.ant = bloqueVacio
                bloqueVacio.sig = A.fin.sig
                bloqueVacio.ant = B.fin
                A.fin.sig = bloqueVacio
            else:
                A.fin.sig.ant = B.fin
                B.fin.sig = A.fin.sig
        else:
            if(A.t4 < B.t4):
                B.fin.definirEspacioVacio(B.t3, A.t4)
                area1.vuelos.cantBloques += 1
                A.fin.sig.ant = B.fin
                B.fin.sig = A.fin.sig
            else:
                A.fin.sig.ant = B.fin.ant
                B.fin.sig = A.fin.sig