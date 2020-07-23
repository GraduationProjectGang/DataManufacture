import json
import time
import pprint
from openpyxl import Workbook
from ast import literal_eval
from dataclasses import dataclass
import numpy as np
from datetime import datetime
import time
import csv
import tensorflow as tf
import ast
import matplotlib.pyplot as plt

filePath_data = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\trainingData.csv'
filePath_stress = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\stressData.csv'

trainingData_x = []
trainingData_y = []

with open(filePath_data, encoding= 'UTF-8') as file:
       trainingData = []
       data = csv.reader(file)
       for object in data:
              trainingData.append(object)
              # print(object)

       trainingData_temp = []
       for item in trainingData:
              for each in item:
                     
                     if len(each) == 0:
                            print("im gang")
                     else:
                            trainingData_temp.append(ast.literal_eval(each))
                     # print(each)

       # trainingData_temp = ast.literal_eval(trainingData)
                     

print(len(trainingData_temp))
y = []
       
with open(filePath_stress, encoding= 'UTF-8') as file:
       data = csv.reader(file)
       for object in data:
              y.append(object)
              # print(object)
       for item in y:
              for real in item:
                     #print(real)
                     trainingData_y.append(real)

       print(len(trainingData_y))

       real_y = list([])

       for i in range(0, 15555):
              if i % 5 == 0:
                     real_y.append(trainingData_y[i])

       print(real_y)
       
      # print(len(trainingData))

       # for item in trainingData_temp:
       #        if len(temp) == 0:
       #               print("im gang")
       #        else:
       #               trainingData_y = np.ndarray(temp)


print(type(trainingData_x))
print(type(trainingData_y))

       # 훈련셋과 검증셋 분리
x_val = trainingData_x[3000:]
y_val = trainingData_y[3000:]
x_train = trainingData_x[:3000]
y_train = trainingData_y[:3000]

# 2. 모델 구성하기
model = Sequential()
model.add(Embedding(max_features, 128))
model.add(LSTM(128))
model.add(Dense(46, activation='softmax'))

# 3. 모델 학습과정 설정하기
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 4. 모델 학습시키기
hist = model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_val, y_val))

# 5. 학습과정 살펴보기

fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')
loss_ax.set_ylim([0.0, 3.0])

acc_ax.plot(hist.history['acc'], 'b', label='train acc')
acc_ax.plot(hist.history['val_acc'], 'g', label='val acc')
acc_ax.set_ylim([0.0, 1.0])

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

# 6. 모델 평가하기
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=64)
print('## evaluation loss and_metrics ##')
print(loss_and_metrics)