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

def main ():

    start = datetime.now()
    s=corrida ()
    end = datetime.now()

    f= open("log/Llamadas a API.txt","a+")
    f.write("Fecha: "+ str(datetime.now()) + " - Tiempo de ejecucion: " + str(end-start)+ ".\n")
    fWrite = open("log/jsonAsignacion.txt", "w+")
    fWrite.write(s)
    fWrite.close()

    return(s)

def corrida():
    # r2 = requests.get(url='https://aviation-edge.com/v2/public/timetable?key=949de0-014c14&iataCode=LIM&type=arrival')
    # data = r2.json()
    listaA = ["ArrivalLima190629 - 6pm","ArrivalLima190629 - 7.20pm","ArrivalLima190630 - 5.20pm","ArrivalLima190701 - 5.30pm","ArrivalLima190630 - 6.10pm.txt","ArrivalLima190702 - 1.21am","ArrivalLima190709 - 9.23am", "ArrivalLima190709 - 10.03am"]
    for c in range(len(listaA)):
        listaA[c] += ".txt"
        
    #aleatorizar la muestra
    nRandom = listaA[round(random.random()*(len(listaA)-1))]
    print (nRandom)
    with open(nRandom) as json_file:  #listaA[round(random.random()*3)]
        data = json.loads(json_file.read().replace("\'", "\""))

    data_filtered = list(filter(lambda x : x['status'] != 'landed' and x['status'] != 'cancelled', data))
    data_ignored = list (filter(lambda x: x['status'] == 'cancelled' or x['status'] == 'landed',data))
    listaVuelos = []
    tamanos = ["Pequeno", "Mediano", "Grande"]
    Clases.Vuelo.nVuelo =0
    
    for flight in data_filtered:
        vuelo = Clases.Vuelo()
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
    for area in (x):
        for p in area.vuelos.listaVuelos:
            if (p.ocupado):
                p.vuelo.asignarPuerta(area)
                listaV.append(p.vuelo)
    s=""
    s+= "[ ["
    for i in range(len(listaV)):
        if (i!=0):
            s+= ", "
        vuelo = listaV[i]
        s += "{ \"numeroVuelo\": \""+ str(vuelo.iata) \
            + "\", \"nombreAerolinea\": \""+ str(vuelo.avion.tAerolinea.nombre) \
            + "\", \"tamañoAvion\": \""+ str(vuelo.avion.tipoAvion.tamano) \
            + "\", \"estado\": \""+ str(vuelo.estado) \
            + "\", \"iataProcedencia\": \""+ str(vuelo.aeropuertoOrigen.iata) \
            + "\", \"idArea\": \""+ str(vuelo.area.idArea) \
            + "\", \"tipoArea\": \""+ str(vuelo.area.tipoArea) \
            + "\", \"tamanoArea\": \""+ str(vuelo.area.tamano) \
            + "\", \"tiempoProgramado\": \""+ str(vuelo.tiempoProgramado) \
            + "\", \"tiempoEstimado\": \""+ str(vuelo.tiempoEstimado) \
            + "\", \"tiempoLlegada\": \""+ str(vuelo.tiempoLlegada) + "\" }" 
    s+="], "
    
    for d in data_ignored:
        d['idArea'] = None
        d['tipoArea'] = None
        d['tamanoArea'] = None

    s+=json.dumps(data_ignored)
    s+=", ["

    for i in range(len(x)):
        if(i!=0):
            s+=","
        s+=x[i].imprimirLista()

    s+="] ] "
    
    return s

if __name__ == '__main__':
    main()