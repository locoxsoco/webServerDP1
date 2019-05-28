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

    corrida ()
    #sys.stdout = sys.__stdout__
    return(s.getvalue())

def corrida():
    #r2 = requests.get(url='https://aviation-edge.com/v2/public/timetable?key=a24d93-2501aa&iataCode=LIM&type=arrival')
    #data = r2.json()
    
    with open("ArrivalLima190504.txt") as json_file:  
        data = json.loads(json_file.read().replace("\'", "\""))

    data_filtered = list(filter(lambda x : x['status'] != 'landed' and x['status'] != 'cancelled', data))
    listaVuelos = []
    Clases.Vuelo.nVuelo =0
    i =0
    for flight in data_filtered:
        i +=1
        vuelo = Clases.Vuelo()
        jsonDestino = flight ['arrival']
        anho = int(jsonDestino['scheduledTime'][0:4])
        mes = int(jsonDestino['scheduledTime'][5:7])
        dia = int(jsonDestino['scheduledTime'][8:10])
        hora = int(jsonDestino['scheduledTime'][11:13])
        minuto = int(jsonDestino['scheduledTime'][14:16])
        segundo = int(jsonDestino['scheduledTime'][17:19])
        vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                   hour=hora, minute=minuto, second=segundo))
        vuelo.setEstado(flight['status'])
        if (vuelo.estado=="active"):
            try:
                anho = int(jsonDestino['scheduledTime'][0:4])
                mes = int(jsonDestino['scheduledTime'][5:7])
                dia = int(jsonDestino['scheduledTime'][8:10])
                hora = int(jsonDestino['scheduledTime'][11:13])
                minuto = int(jsonDestino['scheduledTime'][14:16])
                segundo = int(jsonDestino['scheduledTime'][17:19])
                vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                           hour=hora, minute=minuto, second=segundo))
                vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                           hour=hora, minute=minuto, second=segundo))
            except:
                pass
            
        jsonVuelo = flight['flight']
        vuelo.addNumeroVuelo(jsonVuelo['number'])
        vuelo.addIata(jsonVuelo['iataNumber'])

        try:
            vuelo.addIcao(jsonVuelo['icaoNumber'])
        except:
            pass

        jsonAerolinea = flight['airline']
        aerolinea =Clases.TAerolinea()
        aerolinea.addIata(jsonAerolinea['iataCode'])
        try:
            aerolinea.addIcao(jsonAerolinea['icaoCode'])
        except:
            pass
        aerolinea.addNombre(jsonAerolinea['name'])

        avion = Clases.Avion()
        avion.addTAerolinea(aerolinea)
        vuelo.setAvion(avion)

        vuelo.asignarIDVuelo()
        listaVuelos.append(vuelo)

    nPuertas = 20
    nZonas = 52
    listaZonas = []
    listaPuertas = []
    for i in range(1,nPuertas+1):
        area2 = Clases.Puerta(2*i,random.random()*79+1, random.random()*59+1,random.random()*499+1,random.random()*499+1,10)
        listaPuertas.append(area2)
        
    for i in range(1,nZonas +1):
        area = Clases.Zona(2*i-1,random.random()*79+1, random.random()*59+1,random.random()*499+1, random.random()*499+1)
        listaZonas.append(area)

    ann = Metaheuristico.Annealer(listaVuelos,listaPuertas,listaZonas)
    x,y = ann.anneal()

    print ("[", end="")
    #print("Puertas")
    for i in x[0]:
        i.imprimirLista()
        print (", ",end="")
    #print("Zonas:")
    cont =0
    for i in x[1]:
        if(cont ==0):
            cont =1
        else:
            print(", ",end="")
        i.imprimirLista() 
    #print("Resultado: " + str(y))
    print (" ]")

    end = time. time()
    #print("Tiempo de ejecución: " + str((end-start)))
    return y

if __name__ == '__main__':
    main()