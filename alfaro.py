from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#!flask/bin/python
from flask import Flask
app = Flask(__name__)
from flask import Flask
from flask import request
app = Flask(__name__)
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
import Annealing
import Metaheuristico
from datetime import datetime, date, time, timedelta
@app.route('/getjson', methods=['GET'])
def get():
    f = open("jsonAsignacion.txt","r")
    return (f.read()) 
    # return (str(Annealing.main()))