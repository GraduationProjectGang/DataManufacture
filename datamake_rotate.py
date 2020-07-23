import json
import time
import math
import numpy as np
from datetime import datetime
import ast
from collections import OrderedDict

def transfer(radian):
    ret = (radian * (180 / math.pi))
    if ret >= 0:
        return ret
    else:
        return ret + 360

def posture_x(degree):
    if degree > 0 and degree <= 90:
        return 1
    elif degree > 90 and degree <= 120:
        return 2
    elif degree > 120 and degree <= 180:
        return 3
    else:
        return 0

def posture_y(degree):
    if degree >= 240 and degree <= 300:
        return 2
    elif degree >= 60 and degree <= 120:
        return 2
    elif degree <= 270:
        return 1
    elif degree >= 30:
        return 1
    elif degree >= 180 and degree <= 210:
        return 1
    else:
        return 0

jsonPath = 'C:\\Users\\sejin\\Documents\\GitHub\\DataManufacture\\datacollect.json'
file_path = 'C:\\Users\\sejin\\Documents\\GitHub\\DataManufacture\\rotate_coroutine.json'

with open(jsonPath, encoding= 'UTF-8') as json_file:
    usersData = json.load(json_file)
    users = usersData['user']

    data = OrderedDict()

    for userKey in users:

        data[userKey] = {}
        userName = ''

        stressCountList = list([])
        stressTimestampList = list([])

        for StressCount in users[userKey]:
            if StressCount == 'stress':
                for stresskey in users[userKey][StressCount]:
                    for stressInfo in users[userKey][StressCount][stresskey]:
                        if stressInfo == 'timestamp':
                            temp = int(int(users[userKey][StressCount][stresskey][stressInfo]) / 1000)
                            stressTimestampList.append(temp)
                        elif stressInfo == 'stressCount':
                            stressCountList.append(users[userKey][StressCount][stresskey][stressInfo])

        for rotationVector in users[userKey]:

            if rotationVector == 'rotatevector':
                stressCount_index = 0
                vector_index = 0

                for rotateVecKey in users[userKey][rotationVector]:

                    data_x = np.array([])
                    data_y = np.array([])
                    std_x = 0.0
                    std_y = 0.0
                    posture_list = []
                    orientation_list = []
                    pos = 0
                    ori = 0
                    timeStamp = 0

                    x_list = []
                    y_list = []

                    flag = 0

                    for rotateVecInfo in users[userKey][rotationVector][rotateVecKey]:

                        if rotateVecInfo == 'angleList':
                            for veclist in users[userKey][rotationVector][rotateVecKey][rotateVecInfo]:
                                list_data = ast.literal_eval(veclist)
                                x_list.append(list_data[0])
                                y_list.append(list_data[1])
                            
                            data_x = np.array(x_list)
                            data_y = np.array(y_list)

                            std_x = np.std(data_x)
                            std_y = np.std(data_y)

                            bincount_x = [0, 0, 0, 0]
                            bincount_y = [0, 0, 0]

                            for i in x_list:
                                val = posture_x(transfer(i))
                                posture_list.append(val)
                                bincount_x[val] += 1
                                
                            for i in y_list:
                                val = posture_y(transfer(i))
                                orientation_list.append(val)
                                bincount_y[val] += 1

                            pos = 0
                            for i in range(0, 4):
                                if bincount_x[i] > bincount_x[pos]:
                                    pos = i

                            # print(bincount_x)

                            ori = 0
                            for i in range(0, 3):
                                if bincount_y[i] > bincount_y[ori]:
                                    ori = i

                            # print(bincount_y)
                            flag = 1

                        if rotateVecInfo == 'timestamp':
                            dateTime = users[userKey][rotationVector][rotateVecKey][rotateVecInfo]
                            timestamp = time.mktime(datetime.strptime(dateTime, '%Y%m%d.%H:%M:%S').timetuple())
                            timeStamp = timestamp

                            flag = 2
                            # print(flag)

                        if flag == 2:

                            current_stressCount = -1

                            for idx in range(0, (len(stressTimestampList) - 1)):
                                #print(int(timeStamp), " ", int(stressTimestampList[idx]), " ", int(stressTimestampList[idx + 1]))
                                if (int(timeStamp) >= int(stressTimestampList[idx])) and (int(timeStamp) < int(stressTimestampList[idx + 1])):
                                    if (int(timeStamp) - int(stressTimestampList[idx])) > (int(stressTimestampList[idx + 1]) - int(timeStamp)):
                                        current_stressCount = stressCountList[idx + 1]
                                        stressCount_index = idx + 1
                                    else:
                                        current_stressCount = stressCountList[idx]
                                        stressCount_index = idx

                                if idx == 0 and current_stressCount == -1:
                                    current_stressCount = stressCountList[0]
                                
                                if idx == len(stressTimestampList) - 2 and current_stressCount == -1:
                                    #print(int(timeStamp), " ", int(stressTimestampList[idx]), " ", int(stressTimestampList[idx + 1]))
                                    current_stressCount = stressCountList[idx + 1]


                            # if stressCount_index >= len(stressCountList):
                            #     current_stressCount = 8
                            # else:
                            #     current_stressCount = stressCountList[stressCount_index]
                            #     stressCount_index += 1

                            data[userKey][vector_index] = {
                                "posture": int(pos),
                                "posture_accuracy": bincount_x[pos],
                                "std_posture": float(std_x),
                                "orientation": int(ori),
                                "orientation_accuracy": bincount_y[ori],
                                "std_orientation": float(std_y),
                                "timestamp": timeStamp,
                                "stressCount": current_stressCount
                            }

                            posture_list.clear()
                            orientation_list.clear()
                            pos = 0
                            ori = 0
                            timestamp = 0
                            std_x = 0.0
                            std_y = 0.0
                            flag = 0
                            vector_index += 1

        #     if StressCount == 'userName':
        #         userName = users[userKey][StressCount]

        # print(userName, stressCountList)
        # print(userName, stressTimestampList)          
    
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)