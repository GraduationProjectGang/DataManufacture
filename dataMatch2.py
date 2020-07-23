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
import pprint 
import csv   
    
jsonPath = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\data.json'
statspath = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\appstats.json'
dataAll={}
with open(jsonPath, encoding= 'UTF-8') as json_file:
    data = json.load(json_file)
   
with open(statspath, encoding= 'UTF-8') as file:
    statsData = json.load(file)
    
    for userKey in data:
        for item in data[userKey]: #jsonItem - user,timestamp,ifMoving,posture,posture_accuracy,std_posture,orientation
            for user in statsData:
                if userKey == user:
                    for coroutine in statsData[userKey]:
                        
                        index = 0 
                        if item['timestamp'] == statsData[userKey][coroutine]['timestamp']:
                            dataAll[coroutine] = []
                            for apps in statsData[userKey][coroutine]:
                                if len(apps) == 1:#timestamp가 아니라 app이면
                                    temp = statsData[userKey][coroutine][apps]
                                    if temp == 0:
                                        dataAll[coroutine].append([item['user'],item['timestamp'],item['ifMoving'],item['orientation'],item['posture'],item['posture_accuracy'],item['std_posture'],0,0])
                                        # print(dataAll[coroutine][len(dataAll[coroutine]-1)])                            
                                    else:
                                        dataAll[coroutine].append([item['user'],item['timestamp'],item['ifMoving'],item['orientation'],item['posture'],item['posture_accuracy'],item['std_posture'],temp['category'],temp['totalTimeInForeground']])
                                        # print(dataAll[coroutine][len(dataAll[coroutine]-1)])                               
                                    
                                    index += 1

with open('trainingData.csv','w',newline='') as file:
    for i in list(dataAll.values()):
        cw = csv.writer(file)
        cw.writerow(i)