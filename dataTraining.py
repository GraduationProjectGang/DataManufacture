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
       dataArray = [] #all users
       for user in data:
              userArray=[] # 5 coArray Maximum
              for coroutine in data[user]:
                     coArray = [] #coroutineArray
                     for item in coroutine:
                            coArray.append(coroutine[item])
                     userArray.append(coArray)
              dataArray.append(userArray)


       print(len(dataArray))
              
                     

       # #print(type(dataArr))
       # print(dataArr[dataArr.shape[0]-1])
       # print(dataArr.shape)

       # with open('realData.json', 'w') as outfile:
       #          json.dump(data, outfile)
       
       # print(type(dataArr))



 
       
