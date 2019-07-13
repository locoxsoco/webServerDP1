from datetime import datetime, date,time, timedelta
from io import StringIO
from copy import deepcopy,copy

class Avion :
    def __init__ (self,numeroRegistro=None,icao=None,tipoAvion=None,tAerolinea=None):
        pass
    
    def addNumeroRegistro (self,numeroRegistro):
        self.numeroRegistro = numeroRegistro

    def addIata(self, iata):
        self.iata = iata

    def addIcao(self, icao):
        self.icao = icao

    def addTipoAvion(self, tipoAvion):
        self.tipoAvion = tipoAvion

    def addTAerolinea(self, tAerolinea):
        self.tAerolinea = tAerolinea

class Aeropuerto:
    def __init__ (self):
        self.iata = None
        pass

    def addIata(self,iata):
        self.iata = iata

    def addIdAeropuerto(self, idAeropuerto):
        self.idAeropuerto = idAeropuerto

    def addPais (self, pais):
        self.pais = pais

    def addNombre(self,nombre):
        self.nombre = nombre

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
    def __init__(self, idTipoAvion= 0): 
        pass

    def addCapacidad(self,capacidad):
        self.capacidad = capacidad

    def addTamano (self, tamano):
        self.tamano = tamano

    def addIndice ( self,indice):
        self.indice = indice

class Vuelo: 
    nVuelo = 0    
    def __init__ (self,  estado = None, avion =None,tiempoEstimado =None,tiempoProgramado=None, \
        tiempoLlegada=None,  icao=None, iata=None, \
        numeroVuelo=None,estaEnTierra=None,latitud=None,longitud=None, \
        altura=None, direccion=None, velocidadHorizontal=None, velocidadVertical=None,
        aeropuertoOrigen = None):
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

    def setLlego (self, llego):
        self.llego = llego

    def setEstado(self,estado):
        self.estado = estado

    def setAvion (self,avion):
        self.avion=avion

    def setTiempoEstimado (self,tiempoEstimado):
        self.tiempoEstimado = tiempoEstimado

    def setTiempoProgramado (self,tiempoProgramado):
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

    def asignarPuerta (self, area):
        self.area = area 

    def asignarIDVuelo(self):
        Vuelo.nVuelo +=1
        self.idVuelo = Vuelo.nVuelo

class BloqueVuelo:
    def __init__(self):
        self.vuelo = None
        self.ocupado=None
        self.tiempoInicio = None
        self.tiempoFin = None

    def addVuelo(self,vuelo,tiempo):
        self.vuelo = vuelo
        self.ocupado = True
        self.tiempoInicio = tiempo - timedelta(hours =1)
        self.tiempoFin = tiempo + timedelta(hours=2)

    def definirEspacioVacio(self, tiempoInicio, tiempoFin):
        self.vuelo = None
        self.tiempoInicio = tiempoInicio
        self.tiempoFin=tiempoFin
        self.ocupado=False

class ListaVuelos:
    def __init__ (self):
        bloqueInicial = BloqueVuelo()
        self.tiempoInicio= datetime(year=2019,month =1,day=1,\
            hour=0,minute=0,second=0)
        self.tiempoFin= datetime(year=2020,month =1,day=1,\
            hour=0,minute=0,second=0)

        bloqueInicial.definirEspacioVacio(self.tiempoInicio,self.tiempoFin)
        self.listaVuelos =[] 
        self.listaVuelos.append(bloqueInicial)
        self.cantidad=0
        
    def insertarBloque (self, bloque):
        for p in self.listaVuelos:
            if(p.tiempoInicio > bloque.tiempoInicio):
                break
            if (not p.ocupado and p.tiempoInicio <= bloque.tiempoInicio and p.tiempoFin >= bloque.tiempoFin):
                indice = self.listaVuelos.index(p)
                if (p.tiempoInicio != bloque.tiempoInicio and p.tiempoFin != bloque.tiempoFin):
                    bloqueAnt = BloqueVuelo()
                    bloqueAnt.definirEspacioVacio(p.tiempoInicio,bloque.tiempoInicio)
                    self.listaVuelos.insert(indice, bloqueAnt)
                    bloqueSig = BloqueVuelo()
                    bloqueSig.definirEspacioVacio(bloque.tiempoFin,p.tiempoFin)
                    self.listaVuelos.insert(indice+2,bloqueSig)
                    self.listaVuelos[indice+1].addVuelo(bloque.vuelo,bloque.vuelo.tiempoLlegada)
                    
                elif (p.tiempoInicio != bloque.tiempoInicio):
                    bloqueAnt = BloqueVuelo()
                    bloqueAnt.definirEspacioVacio(p.tiempoInicio,bloque.tiempoInicio)
                    self.listaVuelos.insert(indice, bloqueAnt)
                    self.listaVuelos[indice+1].addVuelo(bloque.vuelo,bloque.vuelo.tiempoLlegada)

                elif (p.tiempoFin != bloque.tiempoFin):
                    bloqueSig = BloqueVuelo()
                    bloqueSig.definirEspacioVacio(bloque.tiempoFin,p.tiempoFin)
                    self.listaVuelos.insert(indice+1,bloqueSig)
                    self.listaVuelos[indice].addVuelo(bloque.vuelo,bloque.vuelo.tiempoLlegada)
                else:
                    self.listaVuelos[indice].addVuelo(bloque.vuelo,bloque.vuelo.tiempoLlegada)
                self.cantidad +=1
                return 1
        return -1

class Area: 
    def __init__ (self, tipoArea, tamano, idArea, coordenadaXCentro=0.0, coordenadaYCentro=0.0):
        self.idArea = idArea
        self.tipoArea = tipoArea
        self.tamano = tamano
        self.vuelos = ListaVuelos()
        
    def addIndice(self, indice):
        self.indice = indice

    def insertarVuelo(self, vuelo,tiempo):
        if(self.indice < vuelo.avion.tipoAvion.indice):
            return -1
        bloque = BloqueVuelo()
        bloque.addVuelo(vuelo,tiempo)
        if (self.vuelos.insertarBloque(bloque) != -1 ):
            bloque.vuelo.asignarPuerta(self)
            return 1
        else:
            return -1

    def imprimirLista(self):
        s="{ \"tipoArea\": \""+ self.tipoArea + "\", \"idArea\": \""+str(self.idArea) + "\", \"tamano\": \""+ self.tamano + "\", "
        s+="\"vuelos\": [ "
        f = 0
        for p in self.vuelos.listaVuelos:
            if (p.ocupado):
                if (f==0):
                    f=1
                else:
                    s+=", "
            # if (p.ocupado):
                s+="{ \"numeroVuelo\": \""+ str(p.vuelo.iata) \
                    + "\", \"nombreAerolinea\": \""+ str(p.vuelo.avion.tAerolinea.nombre) \
                    + "\", \"estado\": \""+ str(p.vuelo.estado) \
                    + "\", \"iataProcedencia\": \""+ str(p.vuelo.aeropuertoOrigen.iata) \
                    + "\", \"TiempoEstimado\": \""+ str(p.vuelo.tiempoEstimado) \
                    + "\", \"TiempoLlegada\": \""+ str(p.vuelo.tiempoLlegada) + "\" }" 
            # else:
            #     s+="{ \"TiempoINI\": \""+ str(p.tiempoInicio) \
            #        + "\", \"TiempoFIN\": \""+ str(p.tiempoFin) + "\" }"
        s+=" ] }"
        return s

    def removeVuelo(self,bloque):
        indice = self.vuelos.listaVuelos.index(bloque)
        # se asume que en la eliminación nunca está al inicio o al final, porque el tiempo es "infinito"
        if (not self.vuelos.listaVuelos[indice-1].ocupado and not self.vuelos.listaVuelos[indice+1].ocupado):
            self.vuelos.listaVuelos[indice-1].definirEspacioVacio(self.vuelos.listaVuelos[indice-1].tiempoInicio, \
                self.vuelos.listaVuelos[indice+1].tiempoFin)
            self.vuelos.listaVuelos.pop(indice+1)
            self.vuelos.listaVuelos.pop(indice)
        elif (not self.vuelos.listaVuelos[indice-1].ocupado) :
            self.vuelos.listaVuelos[indice-1].definirEspacioVacio(self.vuelos.listaVuelos[indice-1].tiempoInicio, \
                bloque.tiempoFin)
            self.vuelos.listaVuelos.pop(indice)
        elif ( not self.vuelos.listaVuelos[indice+1].ocupado) :
            self.vuelos.listaVuelos[indice+1].definirEspacioVacio(bloque.tiempoInicio, \
                self.vuelos.listaVuelos[indice+1].tiempoFin)
            self.vuelos.listaVuelos.pop(indice)
        else:
            bloqueVacio = BloqueVuelo()
            bloqueVacio.definirEspacioVacio(bloque.tiempoInicio, bloque.tiempoFin)
            self.vuelos.listaVuelos.pop(indice)
            self.vuelos.listaVuelos.insert(indice,bloqueVacio)
        self.vuelos.cantidad -=1
        

class Zona(Area):
    def __init__ (self, tipoArea, tamano, idArea=0, coordenadaXCentro=0.0, \
        coordenadaYCentro=0.0):
        Area.__init__(self,  tipoArea,tamano, idArea,  coordenadaXCentro, coordenadaYCentro)

class Manga(Area):
    def __init__ (self, tipoArea, tamano, idArea=0, coordenadaXCentro=0.0, \
        coordenadaYCentro=0.0, velocidadDesembarco = 0.0):
        Area.__init__(self, tipoArea,tamano, idArea,  coordenadaXCentro, coordenadaYCentro)
        self.velocidadDesembarco = velocidadDesembarco

class Intervalo(object):
    def __init__(self, listaVuelos, bloque):
        self.listaVuelos = copy(listaVuelos)
        indice = listaVuelos.index(bloque)
        if (not self.listaVuelos[indice-1].ocupado): 
            self.inicio = self.listaVuelos[indice-1]
            self.t1 = self.listaVuelos[indice-1].tiempoInicio
        else:
            self.inicio = self.listaVuelos[indice]
            self.t1 = self.listaVuelos[indice].tiempoInicio

        self.t2 = self.listaVuelos[indice].tiempoInicio
        self.t3 = self.listaVuelos[indice].tiempoFin

        if( not self.listaVuelos[indice+1].ocupado): 
            self.fin = self.listaVuelos[indice+1]
            self.t4 = self.listaVuelos[indice+1].tiempoFin
        else:
            self.fin = self.listaVuelos[indice]
            self.t4 = self.listaVuelos[indice].tiempoFin
        self.cantidad = 1

    def extendLeft(self):
        indice = self.listaVuelos.index(self.inicio)
        if (indice ==0 ):
            return False
        elif(self.listaVuelos[indice-1].vuelo.llego is True):
            return False
        else:            
            self.inicio = self.listaVuelos[indice-1]
            self.t2 = self.inicio.tiempoInicio
            if (not self.listaVuelos[indice-2].ocupado):
                self.inicio = self.listaVuelos[indice-2]
            self.t1 = self.inicio.tiempoInicio
            self.cantidad +=1
            return True

    def extendRight(self):
        indice = self.listaVuelos.index(self.fin)
        if indice == (len(self.listaVuelos)-1) :
            return False
        elif (self.listaVuelos[indice+1].vuelo.llego is True):
            return False
        else:
            self.fin=self.listaVuelos[indice+1]
            self.t3 = self.fin.tiempoFin
            if(not self.listaVuelos[indice+2].ocupado):
                self.fin = self.listaVuelos[indice+2]
            self.t4 = self.fin.tiempoFin   
            self.cantidad +=1
            return True