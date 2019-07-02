from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#!flask/bin/python
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
from datetime import datetime, date, time, timedelta

@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    return response

@application.route('/getjson', methods=['GET'])
def get():
    # f = open("jsonAsignacion.txt","r")
    # return (f.read()) 
    return (str(Main.main()))

application.run("192.168.214.177", port=5000, debug=True)