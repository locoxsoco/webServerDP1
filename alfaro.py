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

@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response

@application.route('/asignarVuelos', methods=['GET'])
def asignarVuelos(): 
    return (str(Main.main()))

@application.route('/cargarVuelos', methods=['GET'])
def cargarVuelos():
    #Lectura de Mangas y Zonas
    tamanos = ["Pequeño", "Mediano", "Grande"]
    listaAreas = []

    mydb = mysql.connector.connect(
        host="localhost",
        user="inf226",
        passwd="legion@666",
        database="inf226",
        port="3307"
    )
    
    cursor = mydb.cursor(dictionary=True)
    ssql = "SELECT * FROM tarea"
    cursor.execute(ssql)
    resultado = cursor.fetchall()
    cursor.close()

    for i in range(len(resultado)):
        indice = 0
        for j in tamanos:
            if (j == resultado[i]['tamano']):
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
    #leerVuelos de API o de log\Vuelos.txt, o de lo que me mande el JAVA
   
    with open("test/Vuelos.txt") as json_file: 
        data = json.loads(json_file.read().replace("\'", "\""))

    listaVuelos=[]
    i=0
    for flight in data:
        i+=1
        jsonOrigen = flight['departure']
        jsonAvion = flight['aircraft']
        jsonAerolinea = flight['airline']
        jsonVuelo = flight['flight']

        vuelo = Clases.Vuelo()
        vuelo.addIata(jsonVuelo['iataNumber'])
        vuelo.addNumeroVuelo(jsonVuelo['number'])

        aeropuerto = Clases.Aeropuerto()
        aeropuerto.addIata(jsonOrigen['iataCode'])
        vuelo.addAeropuertoOrigen(aeropuerto)

        aerolinea =Clases.TAerolinea()
        aerolinea.addIata(jsonAerolinea['iataCode'])

        tipoAvion = Clases.TipoAvion()
        indice = round(random.random()*2) #BD
        tipoAvion.addTamano(tamanos[indice])
        tipoAvion.addIndice(indice)

        avion = Clases.Avion()
        avion.addIata(jsonAvion['iataCode'])
        avion.addNumeroRegistro(jsonAvion['regNumber'])
        avion.addTAerolinea(aerolinea)
        avion.addTipoAvion(tipoAvion)
        vuelo.setAvion(avion)

        listaVuelos.append(vuelo)

    #cargarBD y guardar en log\Vuelos_Simulador.txt
    log =""
    cursor = mydb.cursor(dictionary=True)
    ssql = "SELECT * FROM tavion"
    cursor.execute(ssql)
    aviones = cursor.fetchall()
    hashAviones = dict()
    for idAvion in range(len(aviones)):
        hashAviones[aviones[idAvion]['id_Avion']]=aviones[idAvion]

    ssql = "SELECT * FROM tciudad_aeropuerto"
    cursor.execute(ssql)
    aeropuertos = cursor.fetchall()
    hashAeropuertos = dict()
    for idAeropuerto in range(len(aeropuertos)):
        hashAeropuertos[aeropuertos[idAeropuerto]['id_Aeropuerto']]=aeropuertos[idAeropuerto] 

    for vuelo in listaVuelos: #area #avion #puerto de origen
        try:
            pass
    # ssql = "SELECT * FROM tavion WHERE iata = "+ vuelo.avion.iata
            # idAvion = avion['id_Avion']
        except:
            idAvion = 0
            log += "No existe registro en BD del avion: "+ str(vuelo.avion.iata)+ "\n"

        try: 
            ssql = "SELECT * FROM tciudad_aeropuerto WHERE = iata = "+vuelo.aeropuerto.iata+"\n"
            cursor.execute(ssql)
            cursor.execute(ssql)
            avion = cursor.fetchone()
        except:
            pass
        # ssql = "INSERT INTO tvuelo ("

    cursor.close()

    fWrite = open("test/Vuelos_Simulador.txt", "w+")
    return log

@application.route('/addVuelo', methods=['POST'])
def addVuelo():
    return

@application.route('/removeVuelo', methods=['POST'])
def removeVuelo():
    return

application.run("192.168.214.177", port=9000, debug=True) #192.168.214.177