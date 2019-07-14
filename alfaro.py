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

class Configuracion:    
    puerto = 9000
    simulacion = True

@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response

@application.route('/estaSimulando', methods=['GET'])
def modoSimulacion(): 
    return str(Configuracion.simulacion)

@application.route('/asignarVuelos', methods=['GET'])
def asignarVuelos(): 
    resultado = str(Main.main())
    print ("Enviado a: " + request.remote_addr + " por el puerto: "+ str(Configuracion.puerto))
    return (resultado)

@application.route('/cargarVuelos/<cargaMasiva>', methods=['POST'])
def cargarVuelos(cargaMasiva):
    Configuracion.simulacion = cargaMasiva
    tamanos = ["Pequeno", "Mediano", "Grande"]
    # try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="inf226",
        passwd="legion@666",
        database="inf226",
        port="3307"
    )
    print("xd")
    #Lectura de Mangas y Zonas
    cursor = mydb.cursor(dictionary=True)
    ssql = "SELECT * FROM tarea WHERE es_eliminado = 0"
    cursor.execute(ssql)
    resultado = cursor.fetchall()
    cursor.close()

    #Lectura de aviones
    cursor = mydb.cursor(dictionary=True)
    ssql = "SELECT * FROM tavion WHERE es_eliminado = 0"
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
    ssql = "SELECT * FROM ttipo_avion WHERE es_eliminado = 0"
    cursor.execute(ssql)
    tAviones = cursor.fetchall()
    hashTAviones = dict()
    for idTAviones in range(len(tAviones)):
        hashTAviones[tAviones[idTAviones]['id_tipo_avion']]=tAviones[idTAviones] 
    # except: 
    #     return "Error de conexión con base de datos"
    cursor.close()

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
        with open("ArrivalLima190713 - 11.53am.txt") as json_file:
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
    cursor = mydb.cursor()
    for indiceVuelo in range(len(listaVuelos)): #area #avion #puerto de origen
        vuelo = listaVuelos[indiceVuelo]
        #encontrar avion
        try:
            avionBD = hashAviones[vuelo.avion.iata]
            indiceAvion = avionBD['id_Avion']
            indiceTAvionBD = avionBD['ttipo_avion_id_tipo_avion']
            tAvionBD = hashTAviones[indiceTAvionBD]

            #encontrar tipo avion
            tipoAvion = Clases.TipoAvion()
            indice = 0
            for j in tamanos:
                if (j == tAvionBD['tamano']):
                    break
                indice +=1
        except:
            try:
                avionBD = hashAviones['000']
                indiceAvion = avionBD['id_Avion']
            except:
                return "No existe el avión base de iata 000"
            indiceTAvionBD = avionBD['ttipo_avion_id_tipo_avion']
            tAvionBD = hashTAviones[indiceTAvionBD]

            #encontrar tipo avion
            tipoAvion = Clases.TipoAvion()
            indice = 0
            for j in tamanos:
                if (j == tAvionBD['tamano']):
                    break
                indice +=1
            log += "No se ha encontrado el avión con iata: "+ str(vuelo.avion.iata) + \
                ", se registrará el vuelo en base de datos con iataAvion = \'000\' "+ " y cuyo tamano será: " + str(tamanos[indice]) +"\n"
        tipoAvion.addTamano(tamanos[indice])
        tipoAvion.addIndice(indice)
        vuelo.avion.addTipoAvion(tipoAvion)

        #encontrar aeropuerto
        try:
            aeropuertoBD = hashAeropuertos[vuelo.aeropuertoOrigen.iata]
            indiceAeropuerto = aeropuertoBD['id_ciudad']
        except:
            try:
                indiceAeropuerto = hashAeropuertos['00']['id_ciudad']
            except:
                return "No existe el aeropuerto base de iata 00"
            log += "No se ha encontrado el aeropuerto con iata: "+ str(vuelo.aeropuertoOrigen.iata) + \
                ", se registrará el vuelo en base de datos con iataCiudad = \'000\' "
        
        #insertar
        args = [vuelo.iata,vuelo.icao,vuelo.numeroVuelo,vuelo.tiempoProgramado,vuelo.tiempoEstimado,vuelo.tiempoLlegada, vuelo.estado, \
            indiceAvion,indiceAeropuerto,vuelo.idArea,0]
        resultado = cursor.callproc("INSERTAR_VUELO",args)

    cursor.close()

    fWrite = open("test/Vuelos_Simulador.txt", "w+")
    return "Cambio exitoso"

@application.route('/addVuelo/<vuelo>', methods=['POST'])
def addVuelo(vuelo):
    content = request.json 
    return  "Se ha agregado correctamente"

@application.route('/removeVuelo/<int:idVuelo>', methods=['POST'])
def removeVuelo(idVuelo):
    return  "Se ha eliminado correctamente"

application.run("192.168.214.177", port=Configuracion.puerto, debug=True) #192.168.214.177