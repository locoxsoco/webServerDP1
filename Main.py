import math
import random
import sys
import requests
import time
import json
import numpy
import Clases
import Metaheuristico
from datetime import datetime, date, timedelta
from io import StringIO

s = StringIO()

def main ():
    s = StringIO()
    sys.stdout = s

    start = datetime.now()
    corrida ()
    end = datetime.now()

    f= open("log/Llamadas a API.txt","a+")
    f.write("Fecha: "+ str(datetime.now()) + " - Tiempo de ejecucion: " + str(end-start)+ ".\n")
    fWrite = open("log/jsonAsignacion.txt", "w+")
    fWrite.write(s.getvalue())
    fWrite.close()

    # sys.stdout = sys.__stdout__
    #print(s.getvalue())

    return(s.getvalue())
    #sys.stdout = sys.__stdout__

def corrida():
    # r2 = requests.get(url='https://aviation-edge.com/v2/public/timetable?key=949de0-014c14&iataCode=LIM&type=arrival')
    # data = r2.json()
    listaA = ["ArrivalLima190504.txt","ArrivalLima190505.txt","ArrivalLima190506.txt","ArrivalLima190507.txt"]
    with open(listaA[round(random.random()*3)]) as json_file:  #listaA[round(random.random()*3)]
        data = json.loads(json_file.read().replace("\'", "\""))

    data_filtered = list(filter(lambda x : x['status'] != 'landed' and x['status'] != 'cancelled', data))
    data_ignored = list (filter(lambda x: x['status'] == 'cancelled' or x['status'] == 'landed',data))
    listaVuelos = []
    tamanos = ["Pequeño", "Mediano", "Grande"]
    Clases.Vuelo.nVuelo =0
    
    #Creación de vuelos
    i = 0
    for flight in data_filtered:
        i +=1
        vuelo = Clases.Vuelo()
        #aleatorizar la muestra
        jsonDestino = flight ['arrival']
        anho = int(jsonDestino['scheduledTime'][0:4])
        mes = int(jsonDestino['scheduledTime'][5:7])
        dia = int(jsonDestino['scheduledTime'][8:10])
        hora = int(jsonDestino['scheduledTime'][11:13])
        minuto = int(jsonDestino['scheduledTime'][14:16])
        segundo = int(jsonDestino['scheduledTime'][17:19])
        vuelo.setTiempoProgramado(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setEstado(flight['status'])
        vuelo.setLlego(False)
        try:
            anho = int(jsonDestino['estimatedTime'][0:4])
            mes = int(jsonDestino['estimatedTime'][5:7])
            dia = int(jsonDestino['estimatedTime'][8:10])
            hora = int(jsonDestino['estimatedTime'][11:13])
            minuto = int(jsonDestino['estimatedTime'][14:16])
            segundo = int(jsonDestino['estimatedTime'][17:19])
            vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                        hour=hora, minute=minuto, second=segundo))
            vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                        hour=hora, minute=minuto, second=segundo))
        except:
            pass

        jsonPartida = flight['departure']
        aeropuerto = Clases.Aeropuerto()
        aeropuerto.addIata(jsonPartida['iataCode'])
        vuelo.addAeropuertoOrigen(aeropuerto)
            
        jsonVuelo = flight['flight']
        vuelo.addNumeroVuelo(jsonVuelo['number'])
        vuelo.addIata(jsonVuelo['iataNumber'])

        jsonAerolinea = flight['airline']
        aerolinea =Clases.TAerolinea()
        aerolinea.addIata(jsonAerolinea['iataCode'])
        try:
            aerolinea.addIcao(jsonAerolinea['icaoCode'])
        except:
            pass
        aerolinea.addNombre(jsonAerolinea['name'])

        tipoAvion = Clases.TipoAvion()

        indice = round(random.random()*2)
        tipoAvion.addTamano(tamanos[indice])
        tipoAvion.addIndice(indice)

        avion = Clases.Avion()
        avion.addTAerolinea(aerolinea)
        avion.addTipoAvion(tipoAvion)
        vuelo.setAvion(avion)

        vuelo.asignarIDVuelo()
        listaVuelos.append(vuelo)

    # listaVuelos.sort(key= lambda x: x.tiempoEstimado)
    #print ("Longitud: "+ str(len(listaVuelos)))
    # Creación de zonas y mangas
    nMangas = 19
    nZonas = 52
    
    listaZonas = []
    listaMangas = []
    for i in range(1,nMangas+1):
        indice = round(random.random()*2)
        area2 = Clases.Manga("Manga",tamanos[indice],i, random.random()*499+1,random.random()*499+1,10)
        area2.addIndice(indice)
        listaMangas.append(area2)
        
    for i in range(1,nZonas +1):
        indice = round(random.random()*2)
        area = Clases.Zona("Zona", tamanos[indice], i, random.random()*499+1, random.random()*499+1)
        area.addIndice(indice)
        listaZonas.append(area)

    ## JSON asignacion antigua 

    ann = Metaheuristico.Annealer(listaVuelos,listaMangas,listaZonas)
    x,y = ann.anneal()

    listaV = []
    for area in (x[0]):
        # p = area.vuelos.inicio
        for p in area.vuelos.listaVuelos:
        # while(p is not None):
            if (p.ocupado):
                p.vuelo.asignarPuerta(area)
                listaV.append(p.vuelo)
    # listaV.sort(key= lambda y: y.tiempoLlegada)
    
    #data_ignored.sort(key= lambda y: y['arrival']['estimatedTime'][0:19])
    print ("[ [", end="")
    for i in range(len(listaV)):
        if (i!=0):
            print(", ", end="")
        vuelo = listaV[i]
        print("{ \"numeroVuelo\": \""+ str(vuelo.iata) \
            + "\", \"nombreAerolinea\": \""+ str(vuelo.avion.tAerolinea.nombre) \
            + "\", \"tamañoAvion\": \""+ str(vuelo.avion.tipoAvion.tamano) \
            + "\", \"estado\": \""+ str(vuelo.estado) \
            + "\", \"iataProcedencia\": \""+ str(vuelo.aeropuertoOrigen.iata) \
            + "\", \"idArea\": \""+ str(vuelo.area.idArea) \
            + "\", \"tipoArea\": \""+ str(vuelo.area.tipoArea) \
            + "\", \"tamanoArea\": \""+ str(vuelo.area.tamano) \
            + "\", \"tiempoProgramado\": \""+ str(vuelo.tiempoProgramado) \
            + "\", \"tiempoEstimado\": \""+ str(vuelo.tiempoEstimado) \
            + "\", \"tiempoLlegada\": \""+ str(vuelo.tiempoLlegada) + "\" }",end="") 
    print ("], ", end="")
    
    for s in data_ignored:
        s['idArea'] = None
        s['tipoArea'] = None
        s['tamanoArea'] = None

    print (json.dumps(data_ignored),end="")
    print ( ", [", end="")

    for i in range(len(x[0])):
        if(i!=0):
            print (",", end="")
        x[0][i].imprimirLista()

    print ("] ] ",end="")
    
    return y

if __name__ == '__main__':
    main()