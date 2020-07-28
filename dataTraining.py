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
import tensorflow as tf
import ast
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.datasets import reuters
from keras.utils import np_utils
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.layers import Flatten

max_features = 15000
text_max_words = 120

filePath_data = 'C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\trainingData.csv'
filePath_stress = 'C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\stressData.csv'

trainingData_x = []
trainingData_y = []


with open(filePath_data, encoding= 'UTF-8') as file:
       data = csv.reader(file)

  
       
       for object in data:
              # trainingData_x.append(object)
              # print(object)
              dummy_list = []
              for each in object:
                     each = ast.literal_eval(each)
                     map(float, each)
                     dummy_list.append(each)

                   
                     
        
              trainingData_x.append(dummy_list)
              

       # trainingData_temp = []
       # for item in trainingData:
       #        for each in item:
       #               if each == "":
       #                      print("im gang")
       #               else:
       #                      trainingData_temp.append(ast.literal_eval(each))
       #               # print(each)
       #        print(len(trainingData_x))
       #        trainingData_x.append(trainingData_temp)


y = []
       
with open(filePath_stress, encoding= 'UTF-8') as file:
       data = csv.reader(file)
       for list in data:
              for stressCount in list:
                     trainingData_y.append(float(stressCount))
       
       # for object in data:
       #        y.append(object)
       #        # print(object)
       # for item in y:
       #        for real in item:
       #               #print(real) x
       #               trainingData_y.append(real)




trainingData_x = np.array(trainingData_x)

trainingData_x = trainingData_x / trainingData_x.max(axis=0)
trainingData_x = trainingData_x - trainingData_x.mean(axis=0).reshape(1,5,6)
# trainingData_x = trainingData_x.tolist()

trainingData_y = np.array(trainingData_y)

trainingData_y = trainingData_y / trainingData_y.max()
trainingData_y = trainingData_y - trainingData_y.mean(axis=0).reshape(1)
# trainingData_y = trainingData_y.tolist()

# print(trainingData_x)
print(trainingData_x.shape)

# 훈련셋과 검증셋 분리
# x_train = trainingData_x
# y_train = trainingData_y[3000:]
# x_val = trainingData_x[:3000]
# y_val = trainingData_y[:3000]
x_train,x_val,y_train,y_val = train_test_split(trainingData_x,trainingData_y,test_size = 0.25)
print(len(x_train))
print(len(y_train))
print(len(x_val))
print(len(y_val))
print(x_train[-1])
print(y_train[-1])



# mean = x_train.mean(axis=0)
# std = x_train.std(axis=0)
# x_train = (x_train - mean) / std
# x_train = (x_train - mean) / std # test_data도 train_data의 평균과 표준편차를 이용


# 2. 모델 구성하기
model = Sequential()
model.add(LSTM(128))
model.add(Dense(16,input_shape=(8,),activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(1, activation='softmax'))

# 3. 모델 학습과정 설정하기
model.compile(loss='MSE', optimizer='adam', metrics=['accuracy'])

# 4. 모델 학습시키기
hist = model.fit(x_train, y_train, epochs=30, batch_size=50, validation_data=(x_val, y_val))

# 5. 학습과정 살펴보기


fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')
loss_ax.set_ylim([0.0, 3.0])

acc_ax.plot(hist.history['accuracy'], 'b', label='train acc')
acc_ax.plot(hist.history['val_accuracy'], 'g', label='val acc')
acc_ax.set_ylim([0.0, 1.0])

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

# 6. 모델 평가하기
loss_and_metrics = model.evaluate(x_val, y_val, batch_size=64)
print('## evaluation loss and_metrics ##')
print(loss_and_metrics)