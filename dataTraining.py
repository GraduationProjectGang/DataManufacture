import json
import time
import pprint
from openpyxl import Workbook
from ast import literal_eval
from dataclasses import dataclass
import numpy as np
from datetime import datetime
import time
from rotate import getRotateVec
import csv
import keras


filePath = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\trainingData.csv'

trainingData = []
with open(filePath, encoding= 'UTF-8') as file:
       data = csv.reader(file)

       print(data)
       for object in data:
              trainingData.append(object)
              # print(object)
       



       print(type(trainingData))
       data = np.ndarray(trainingData)
       print(data[data.shape[0]-1])
       print(data.shape)

       # with open('realData.json', 'w') as outfile:
       #          json.dump(data, outfile)
       
       # print(type(dataArr))

       model = keras.models.Sequential()

 
       
