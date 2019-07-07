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

@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response

@application.route('/getjson', methods=['GET'])
def getAsignacion():
    # f = open("jsonAsignacion.txt","r")
    # return (f.read()) 
    return (str(Main.main()))

@application.route('/addvuelo', methods=['POST'])
def addVuelo():
    # f = open("jsonAsignacion.txt","r")
    # return (f.read()) 
    pass

application.run("localhost", port=5000, debug=True)