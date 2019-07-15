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
from copy import deepcopy
class Configuracion(object):    
    puerto = 9000
    simulacion = True
    ncorrida = 0
    listaA = []
    archivoActual = ""
    urlAPI = 'https://aviation-edge.com/v2/public/timetable?key=949de0-014c14&iataCode=LIM&type=arrival'
    for c in range(1,73):
        listaA.append("Set de datos/Set" + str(c) + ".txt")
    listaVuelos = []
    data_ignored = []
    listaAreas =[]

# def actualizarVuelos (cargaMasiva):

@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response

@application.route('/estaSimulando', methods=['GET'])
def modoSimulacion(): 
    return str(Configuracion.simulacion)

@application.route('/asignarVuelos/<simulando>', methods=['GET'])
def asignarVuelos(simulando): 
    carga(simulando)
    print ("Archivo invocado - - [",datetime.now(),"] - - ","vuelos.txt")
    resultado = str(Main.main())
    print ("Enviado a: " + request.remote_addr + " por el puerto: "+ str(Configuracion.puerto))
    return (resultado)

@application.route('/cargarVuelos/<cargaMasiva>', methods=['GET'])
def cargarVuelos(cargaMasiva):
    texto = cargaMasiva.split("&")
    flag_Cambio = texto[0]
    flag_Original = texto[1]
    s = carga(flag_Cambio)
    return s
    # return actualizarVuelos(cargaMasiva) 

@application.route('/addVuelo/<vuelo>', methods=['POST'])
def addVuelo(vuelo):
    content = request.json 
    return  "OK"

@application.route('/removeVuelo/<int:idVuelo>', methods=['GET'])
def removeVuelo(idVuelo):
    return  "OK"

    
def carga (flag_Cambio):
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
        ssql = "SELECT * FROM tarea WHERE es_eliminado = 0 AND tamano <> \'Zero\'"
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
    except: 
        return "Error de conexión con base de datos"
    cursor.close()

    Configuracion.simulacion = flag_Cambio
    tamanos = ["Pequeno", "Mediano", "Grande"]
    listaAreas=[]
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
    Configuracion.listaAreas = deepcopy(listaAreas)
    try:
        f = open("vuelos.txt","w+")
        cursor = mydb.cursor()
        cursor.execute("TRUNCATE TABLE tvuelo")
    except:
        return "Error al borrar tabla o archivo vuelos.txt"
    cursor.close()
    #leerVuelos de API o de lo que se mande de los txt
    listaVuelos=[]
    if (flag_Cambio == "False"):
        try:
            r2 = requests.get(url=Configuracion.urlAPI)
            data = r2.json()
            print("Subiendo Archivo de API Aviation Edge- - [",datetime.now(),"]")
        except:
            with open("test/ArrivalLima190630 - 6.10pm.txt") as json_file:
                data = json.loads(json_file.read().replace("\'", "\""))
            print("Carga de vuelos [",datetime.now(),"] - No hay servicio de aviation-edge, cargando archivo de vuelos \'ArrivalLima190630 - 6.10pm.txt\'")
        
        data_filtered = list(filter(lambda x : x['status'] != 'landed' and x['status'] != 'cancelled', data))
        Configuracion.data_ignored = list (filter(lambda x: x['status'] == 'cancelled' or x['status'] == 'landed',data))
        #carga de vuelos a memoria
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
            avion.addIata(random.choice(list(hashAviones.keys())))
            vuelo.setAvion(avion)

            listaVuelos.append(vuelo)
    else:  
        if (Configuracion.ncorrida > 72):
            Configuracion.ncorrida = 0
        Configuracion.archivoActual = Configuracion.listaA[Configuracion.ncorrida]
        Configuracion.ncorrida +=1  
        with open(Configuracion.archivoActual) as json_file:
            data = json.loads(json_file.read().replace("\'", "\"").replace(" ","").replace("\t"," ").replace("\n"," ")[3:])
        print("Subiendo Archivo - - ",Configuracion.archivoActual)
        #carga de vuelos a memoria
        indiceSet = 'Set' + str(Configuracion.ncorrida)
        data_filtered = list(filter(lambda x : x['status'] != 'landed' and x['status'] != 'cancelled', data[indiceSet]))
        Configuracion.data_ignored = list (filter(lambda x: x['status'] == 'cancelled' or x['status'] == 'landed',data[indiceSet]))

        for flight in data_filtered:
            vuelo = Clases.Vuelo()
            anho = int(flight['arrival__scheduledTime'][0:4])
            mes = int(flight['arrival__scheduledTime'][5:7])
            dia = int(flight['arrival__scheduledTime'][8:10])
            hora = int(flight['arrival__scheduledTime'][11:13])
            minuto = int(flight['arrival__scheduledTime'][14:16])
            segundo = int(flight['arrival__scheduledTime'][17:19])
            vuelo.setTiempoProgramado(datetime(year=anho, month=mes, day=dia, \
                                    hour=hora, minute=minuto, second=segundo))
            vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                    hour=hora, minute=minuto, second=segundo))
            vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                    hour=hora, minute=minuto, second=segundo))
            vuelo.setEstado(flight['status'])
            try:
                anho = int(flight['arrival__estimatedTime'][0:4])
                mes = int(flight['arrival__estimatedTime'][5:7])
                dia = int(flight['arrival__estimatedTime'][8:10])
                hora = int(flight['arrival__estimatedTime'][11:13])
                minuto = int(flight['arrival__estimatedTime'][14:16])
                segundo = int(flight['arrival__estimatedTime'][17:19])
                vuelo.setTiempoEstimado(datetime(year=anho, month=mes, day=dia, \
                                            hour=hora, minute=minuto, second=segundo))
                vuelo.setTiempoLlegada(datetime(year=anho, month=mes, day=dia, \
                                            hour=hora, minute=minuto, second=segundo))
            except:
                pass

            aeropuerto = Clases.Aeropuerto()
            aeropuerto.addIata(flight['departure__iataCode'])
            vuelo.addAeropuertoOrigen(aeropuerto)

            vuelo.addNumeroVuelo(flight['flight__number'])
            vuelo.addIata(flight['flight__iataNumber'])

            aerolinea =Clases.TAerolinea()
            aerolinea.addIata(flight['airline__iataCode'])
            aerolinea.addNombre(flight['airline__name'])

            avion = Clases.Avion()
            avion.addTAerolinea(aerolinea)
            avion.addIata(random.choice(list(hashAviones.keys())))
            # print(avion.iata)
            vuelo.setAvion(avion)

            listaVuelos.append(vuelo)
            
    #cargarBD y guardar en log\Vuelos_Simulador.txt
    listaVuelos.sort(key=lambda x: x.tiempoEstimado)
    log =""
    cursor = mydb.cursor()
    s= "[ [ "
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
                indiceAeropuerto = hashAeropuertos['000']['id_ciudad']
            except:
                return "No existe el aeropuerto base de iata 000"
            log += "No se ha encontrado el aeropuerto con iata: "+ str(vuelo.aeropuertoOrigen.iata) + \
                ", se registrará el vuelo en base de datos con iataCiudad = \'000\' "
        
        #insertar
        try:
            args = [vuelo.iata,vuelo.icao,vuelo.numeroVuelo,vuelo.tiempoProgramado,vuelo.tiempoEstimado, vuelo.estado, \
                indiceAvion,indiceAeropuerto,73,0]
            resultado = cursor.callproc("INSERTAR_VUELO",args)
            listaVuelos[indiceVuelo].idVuelo = resultado[9]
            # print ( "JA")
            if (indiceVuelo!=0):
                s+= ", "
            s += "{ \"numeroVuelo\": \""+ str(vuelo.iata) \
                + "\", \"idVuelo\": \""+ str(vuelo.idVuelo) \
                + "\", \"iataAerolinea\": \""+ str(vuelo.avion.tAerolinea.iata) \
                + "\", \"nombreAerolinea\": \""+ str(vuelo.avion.tAerolinea.nombre) \
                + "\", \"iataAvion\": \""+ str(vuelo.avion.tAerolinea.nombre) \
                + "\", \"indiceAvion\": \""+ str(vuelo.avion.tipoAvion.indice) \
                + "\", \"tamañoAvion\": \""+ str(vuelo.avion.tipoAvion.tamano) \
                + "\", \"estado\": \""+ str(vuelo.estado) \
                + "\", \"iataProcedencia\": \""+ str(vuelo.aeropuertoOrigen.iata) \
                + "\", \"tiempoProgramado\": \""+ str(vuelo.tiempoProgramado) \
                + "\", \"tiempoEstimado\": \""+ str(vuelo.tiempoEstimado) + "\" }" 

        except:
            cursor.close()
            mydb.rollback()
            return "Error al insertar"

    s+="], "    
    for d in Configuracion.data_ignored:
        d['idArea'] = None
        d['tipoArea'] = None
        d['tamanoArea'] = None
    s+=json.dumps(Configuracion.data_ignored)
    s+=", ["
    for i in range(len(Configuracion.listaAreas)):
        if(i!=0):
            s+=","
        s+=Configuracion.listaAreas[i].imprimirLista()
    s+="] ]"

    Configuracion.listaVuelos = deepcopy(listaVuelos)
    f.write(s)
    f.close()
    mydb.commit()
    cursor.close()
    return "OK"

application.run("localhost", port=Configuracion.puerto, debug=True) #192.168.214.177
