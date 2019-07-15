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
from copy import deepcopy

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
    # listaA = ["ArrivalLima190629 - 6pm","ArrivalLima190629 - 7.20pm","ArrivalLima190630 - 5.20pm","ArrivalLima190701 - 5.30pm","ArrivalLima190630 - 6.10pm","ArrivalLima190702 - 1.21am","ArrivalLima190709 - 9.23am", "ArrivalLima190709 - 10.03am"]
        
    # nRandom = listaA[round(random.random()*(len(listaA)-1))]
    listaVuelos = []
    tamanos = ["Pequeno", "Mediano", "Grande"]
    with open("vuelos.txt") as json_file:
        data = json.loads(json_file.read().replace("\'", "\"").replace(" ","").replace("\t"," ").replace("\n"," "))
    #carga de vuelos a memoria
    data_filtered = data[0]
    data_ignored = data[1]
    for flight in data_filtered:
        vuelo = Clases.Vuelo()
        anho = int(flight['tiempoProgramado'][0:4])
        mes = int(flight['tiempoProgramado'][5:7])
        dia = int(flight['tiempoProgramado'][8:10])
        hora = int(flight['tiempoProgramado'][10:12])
        minuto = int(flight['tiempoProgramado'][13:15])
        segundo = int(flight['tiempoProgramado'][16:18])
        vuelo.setTiempoProgramado(datetime(year=anho, month=mes, day=dia, \
                                hour=hora, minute=minuto, second=segundo))
        vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                hour=hora, minute=minuto, second=segundo))
        vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                hour=hora, minute=minuto, second=segundo))
        vuelo.setEstado(flight['estado'])
        try:
            anho = int(flight['tiempoEstimado'][0:4])
            mes = int(flight['tiempoEstimado'][5:7])
            dia = int(flight['tiempoEstimado'][8:10])
            hora = int(flight['tiempoEstimado'][10:12])
            minuto = int(flight['tiempoEstimado'][13:15])
            segundo = int(flight['tiempoEstimado'][16:18])
            vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                        hour=hora, minute=minuto, second=segundo))
            vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                        hour=hora, minute=minuto, second=segundo))
        except:
            pass

        aeropuerto = Clases.Aeropuerto()
        aeropuerto.addIata(flight['iataProcedencia'])
        vuelo.addAeropuertoOrigen(aeropuerto)

        vuelo.addIata(flight['numeroVuelo'])

        aerolinea =Clases.TAerolinea()
        aerolinea.addIata(flight['iataAerolinea'])
        aerolinea.addNombre(flight['nombreAerolinea'])

        tipoAvion = Clases.TipoAvion()
        tipoAvion.addIndice(int(flight['indiceAvion']))
        tipoAvion.addTamano(flight['tamañoAvion'])
        avion = Clases.Avion()
        avion.addTipoAvion(tipoAvion)
        avion.addTAerolinea(aerolinea)
        # print(avion.iata)
        vuelo.setAvion(avion)
        vuelo.setLlego(False)
        listaVuelos.append(vuelo)

    listaAreas = []
    for area in data[2]:
        indice = 0
        for j in range(len(tamanos)):
            if (tamanos[j] == area['tamano']):
                break
            indice +=1
        tipo = area['tipoArea']
        if (tipo == "Manga") :
            area = Clases.Manga("Manga",tamanos[indice], \
                area['idArea'], 0,0)
        elif (tipo =="Zona"):
            area = Clases.Zona("Zona",tamanos[indice], \
                area['idArea'], 0,0)
        area.addIndice(indice)
        listaAreas.append(area)
    
    ## JSON asignacion antigua     
    ann = Metaheuristico.Annealer(listaVuelos,listaAreas)
    x,y = ann.anneal()

    listaV = []
    for area in (x):
        for p in area.vuelos.listaVuelos:
            if (p.ocupado):
                p.vuelo.asignarPuerta(area)
                listaV.append(p.vuelo)
    s= ""
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