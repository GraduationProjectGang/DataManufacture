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

jsonPath = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\data.json'

with open(jsonPath, encoding= 'UTF-8') as json_file:
       data = json.load(json_file)
       print(type(data))
       userData=[]
       for user in data:
              for coroutine in data[user]:
                     print(coroutine)
                     userData.append(coroutine)
       

       dataArr = np.array(userData)
       #print(type(dataArr))
       print(dataArr.shape)

       reshaped = dataArr.reshape(1, dataArr.shape[0],6)
       print(reshaped.shape)

       
       
