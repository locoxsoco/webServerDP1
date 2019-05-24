from datetime import datetime, date,time, timedelta
from io import StringIO

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
            if (not p.ocupado and p.tiempoInicio<= bloque.tiempoInicio and \
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
                    self.cantBloques += 1
                if (p.tiempoFin != bloque.tiempoFin):
                    bloqueSig = BloqueVuelo()
                    bloqueSig.definirEspacioVacio(bloque.tiempoFin,p.tiempoFin)
                    bloqueSig.sig = p.sig
                    self.cantBloques +=1

                if(bloqueAnt is None):
                    self.inicio = bloque
                else:
                    bloqueAnt.sig = bloque
                bloque.sig = bloqueSig
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
            print ("{ \"tipo\": \""+ "puerta\", ",end="")
        else:
            print ("{ \"tipo\": \""+ "zona\", ", end ="")
        print ("\"vuelos\": [ ",end="")
        p=self.vuelos.inicio
        f = 0
        while(p is not None):
            if (p.ocupado):
                #print("\"tiempoInicio\": \""+str(p.tiempoInicio)+ "\", \"tiempoFin\": \""+str(p.tiempoFin)+"\", ",end='')
                if (f==0):
                    f=1
                else:
                    print(", ",end="")
                print("{ \"numeroVuelo\": \""+ str(p.vuelo.numeroVuelo) + "\", \"TiempoLlegada\": \""+ str(p.vuelo.tiempoEstimado)+ "\" }",end="") 
            #else:
            #    print()
            p=p.sig            
        print(" ] }",end="")
        #print("----------------------")

    def removeVuelo(self,bloque):
        p = self.vuelos.inicio
        ant = None
        while (p is not None):
            if(p == bloque):
                if(ant is not None and p.sig is not None):
                    if (not ant.ocupado and not p.sig.ocupado):
                        ant.definirEspacioVacio(ant.tiempoInicio, p.sig.tiempoFin)
                        ant.sig = p.sig.sig
                        self.vuelos.cantBloques -= 1
                    elif (not ant.ocupado):
                        ant.definirEspacioVacio(ant.tiempoInicio,p.tiempoFin)
                        ant.sig = p.sig
                    elif (not p.sig.ocupado):
                        p.sig.definirEspacioVacio(p.tiempoInicio,p.sig.tiempoFin)
                        ant.sig = p.sig
                    else:
                        ant.sig = p.sig

                elif (ant is None):
                    self.vuelos.inicio = p.sig
                elif(p.sig is None):
                    ant.sig = None

                self.vuelos.cantBloques -=1
                self.vuelos.cantidad -=1
                break
            ant = p
            p=p.sig

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
            #self.tiempoLibre = insercion
            return 1
        else:
            return -1

class Manga: 
    def __init__(self):
        pass

    def asignarPuerta(self, puerta):
        self.puerta=puerta
