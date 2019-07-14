from flask import Flask
from flask import request
application = Flask(__name__)

import multiprocessing as mp
import math
import random
import sys
import requests
import time
import json
import numpy
import importlib
import Clases
import Main
import Metaheuristico
import mysql.connector
from datetime import datetime

@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response

@application.route('/asignarVuelos', methods=['GET'])
def asignarVuelos(): 
    return (str(Main.main()))

@application.route('/cargarVuelos/<cargaMasiva>', methods=['POST'])
def cargarVuelos(cargaMasiva):
    tamanos = ["Pequeno", "Mediano", "Grande"]
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="inf226",
            passwd="legion@666",
            database="inf226",
            port="3307"
        )
        #Lectura de Mangas y Zonas
        cursor = mydb.cursor(dictionary=True)
        ssql = "SELECT * FROM tarea"
        cursor.execute(ssql)
        resultado = cursor.fetchall()
        cursor.close()

        #Lectura de aviones
        cursor = mydb.cursor(dictionary=True)
        ssql = "SELECT * FROM tavion"
        cursor.execute(ssql)
        aviones = cursor.fetchall()
        hashAviones = dict()
        for idAvion in range(len(aviones)):
            hashAviones[aviones[idAvion]['iata']]=aviones[idAvion]

        #Lectura de aeropuertos
        cursor = mydb.cursor(dictionary=True)
        ssql = "SELECT * FROM tciudad_aeropuerto"
        cursor.execute(ssql)
        aeropuertos = cursor.fetchall()
        hashAeropuertos = dict()
        for idAeropuerto in range(len(aeropuertos)):
            hashAeropuertos[aeropuertos[idAeropuerto]['iata']]=aeropuertos[idAeropuerto] 
    
        #Lectura de tipoAviones
        cursor = mydb.cursor(dictionary=True)
        ssql = "SELECT * FROM ttipo_avion"
        cursor.execute(ssql)
        tAviones = cursor.fetchall()
        hashTAviones = dict()
        for idTAviones in range(len(tAviones)):
            hashTAviones[aeropuertos[idTAviones]['iata']]=tAviones[idTAviones] 
    except: 
        return "Error de conexión con base de datos"

    listaAreas = []
    for i in range(len(resultado)):
        indice = 0
        for j in range(len(tamanos)):
            if (tamanos[j] == resultado[i]['tamano']):
                break
            indice +=1
        if (resultado[i]['tipo_area'] == "Manga") :
            area = Clases.Manga("Manga",tamanos[indice], \
                resultado[i]['id_area_estacionamiento'], resultado[i]['coordenada_x'],resultado[i]['coordenada_y'])
        elif (resultado[i]['tipo_area']=="Zona"):
            area = Clases.Zona("Zona",tamanos[indice], \
                resultado[i]['id_area_estacionamiento'], resultado[i]['coordenada_x'],resultado[i]['coordenada_y'])
        area.addIndice(indice)
        listaAreas.append(area)

    #leerVuelos de API o de lo que me mande el JAVA
    if (cargaMasiva == "False"):
        try:
            r2 = requests.get(url='https://aviation-edge.com/v2/public/timetable?key=949de0-014c14&iataCode=LIM&type=arrival')
            data = r2.json()
            # data = json.loads(jsonvuelos.replace("\'", "\""))
        except:
            print("Carga de vuelos [",datetime.now(),"] - No hay servicio de aviation-edge, cargando archivo de configuración normal")
    else:    
        with open("ArrivalLima190713 - 11.53am") as json_file:
            data = json.loads(json_file.read().replace("\'", "\""))
    print(data)
    listaVuelos=[]
    i=0
    for flight in data:
        i+=1
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

        avion = Clases.Avion()
        avion.addTAerolinea(aerolinea)
        vuelo.setAvion(avion)

        vuelo.asignarIDVuelo()
        listaVuelos.append(vuelo)

    #cargarBD y guardar en log\Vuelos_Simulador.txt
    log =""

    for indiceVuelo in range(len(listaVuelos)): #area #avion #puerto de origen
        vuelo = listaVuelos[indiceVuelo]
        #buscar ids
        tipoAvion = Clases.TipoAvion()
        indice = 0
        for j in tamanos:
            if (j == "de base de datos"):
                break
            indice +=1
        tipoAvion.addTamano(tamanos[indice])
        tipoAvion.addIndice(indice)
        vuelo.avion.addTipoAvion(tipoAvion)


        #insertar
        args = [vuelo.iata,vuelo.icao,vuelo.numeroVuelo,vuelo.tiempoProgramado,vuelo.tiempoEstimado,vuelo.tiempoLlegada, vuelo.estado, \
            vuelo.idAvion,vuelo.idAeropuerto,vuelo.idArea,0]
        resultado = cursor.callproc("INSERTAR_VUELO",args)

    cursor.close()

    fWrite = open("test/Vuelos_Simulador.txt", "w+")
    return log

@application.route('/addVuelo/<vuelo>', methods=['POST'])
def addVuelo(vuelo):
    content = request.json 
    return  "Se ha agregado correctamente"

@application.route('/removeVuelo/<int:idVuelo>', methods=['POST'])
def removeVuelo(idVuelo):
    return  "Se ha eliminado correctamente"

application.run("192.168.214.177", port=9000, debug=True) #192.168.214.177