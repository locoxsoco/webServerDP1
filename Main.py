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
sys.stdout = s

def main ():
    start = time.time()
    corrida ()
    end = time. time()

    f= open("Llamadas a API.txt","a+")
    # fWrite = open ("jsonAsignacion.txt", "w")
    f.write("Fecha: "+ str(datetime.now()) + " - Tiempo de ejecucion: " + str((end-start))+ " segundos.\n")
    # fWrite.write(s.getvalue())
    # fWrite.close()

    sys.stdout = sys.__stdout__
    print(s.getvalue())
    return(s.getvalue())
    #sys.stdout = sys.__stdout__

def corrida():
    #r2 = requests.get(url='https://aviation-edge.com/v2/public/timetable?key=a24d93-2501aa&iataCode=LIM&type=arrival')
    #data = r2.json()
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
        if (vuelo.estado=="active"):
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
        tipoAvion.addTamano(tamanos[round(random.random()*2)])

        avion = Clases.Avion()
        avion.addTAerolinea(aerolinea)
        avion.addTipoAvion(tipoAvion)
        vuelo.setAvion(avion)

        vuelo.asignarIDVuelo()
        listaVuelos.append(vuelo)

    listaVuelos.sort(key= lambda x: x.tiempoEstimado)
    #print ("Longitud: "+ str(len(listaVuelos)))
    # Creación de zonas y puertas
    nPuertas = 20
    nZonas = 52
    
    listaZonas = []
    listaPuertas = []
    for i in range(1,nPuertas+1):
        area2 = Clases.Puerta("Puerta",tamanos[round(random.random()*2)],i, random.random()*499+1,random.random()*499+1,10)
        listaPuertas.append(area2)
        
    for i in range(1,nZonas +1):
        area = Clases.Zona("Zona", tamanos[round(random.random()*2)], i, random.random()*499+1, random.random()*499+1)
        listaZonas.append(area)

    ann = Metaheuristico.Annealer(listaVuelos,listaPuertas,listaZonas)
    x,y = ann.anneal()
    # a = x[0]+x[1]
    # z=0
    # for k in a:
    #    z += k.vuelos.cantidad
    # print ( "Cantidad: ", z) 

    x[2].sort(key= lambda y: y.tiempoEstimado)
    data_ignored.sort(key= lambda y: y['arrival']['estimatedTime'][0:19])
    print ("[ [", end="")
    for i in range(len(x[2])):
        if (i!=0):
            print(", ", end="")
        vuelo = x[2][i]
        print("{ \"numeroVuelo\": \""+ str(vuelo.iata) \
            + "\", \"nombreAerolinea\": \""+ str(vuelo.avion.tAerolinea.nombre) \
            + "\", \"estado\": \""+ str(vuelo.estado) \
            + "\", \"iataProcedencia\": \""+ str(vuelo.aeropuertoOrigen.iata) \
            + "\", \"puertaAsignada\": \""+ str(vuelo.area.tipoArea)+" " + str(vuelo.area.idArea) \
            + "\", \"tamanoPuerta\": \""+ str(vuelo.area.tamano) \
            + "\", \"tiempoProgramado\": \""+ str(vuelo.tiempoProgramado) \
            + "\", \"tiempoEstimado\": \""+ str(vuelo.tiempoEstimado) \
            + "\", \"tiempoLlegada\": \""+ str(vuelo.tiempoLlegada) + "\" }",end="") 
    print ("], ", end="")
    
    print (json.dumps(data_ignored),end="")

    print ("] ",end="")
    
    return y

if __name__ == '__main__':
    main()