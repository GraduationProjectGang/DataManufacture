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
       userDataArray=[]
       for user in data:
              for coroutine in data[user]:
                     # print(coroutine)
                     userData = []
                     for item in coroutine:
                            userData.append(coroutine[item])
                     userDataArray.append(userData)
                     # print(userDataArray)
                     


       dataArr = np.array(userDataArray)
       #print(type(dataArr))
       print(dataArr[dataArr.shape[0]-1])
       print(dataArr.shape)    
       
