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
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets

np.random.seed(5)

max_features = 15000
text_max_words = 120

filePath_data = 'C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\trainingData.csv'
filePath_stress = 'C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\stressData.csv'

trainingData_x = []
trainingData_y = []


with open(filePath_data, encoding= 'UTF-8') as file:
       data = csv.reader(file)

  
       
       # for object in data:
       #        dummy_list = []
       #        for each in object:
       #               each = ast.literal_eval(each)
       #               map(float, each)
       #               dummy_list.append(each)
       #        trainingData_x.append(dummy_list)

       for object in data:
              for each in object:
                     each = ast.literal_eval(each)
                     map(float, each)
                     trainingData_x.append(each)

       

y = []
       
with open(filePath_stress, encoding= 'UTF-8') as file:
       data = csv.reader(file)
       for list in data:
              for stressCount in list:
                     trainingData_y.append(float(stressCount))




trainingData_x = np.array(trainingData_x)

trainingData_x = trainingData_x / trainingData_x.max(axis=0)
#trainingData_x = trainingData_x - trainingData_x.mean(axis=0).reshape(1,5,5)
trainingData_x = trainingData_x - trainingData_x.mean(axis=0)
trainingData_x = trainingData_x.tolist()

trainingData_y = np.array(trainingData_y)

trainingData_y = trainingData_y / trainingData_y.max()
trainingData_y = trainingData_y - trainingData_y.mean(axis=0).reshape(1)
trainingData_y = trainingData_y.tolist()

# print(trainingData_x)
#print(trainingData_x.shape)

real_y = []

idx = 0

for i in range(0, len(trainingData_x)):
       if i % 5 == 0 and i != 0:
              idx += 1
       real_y.append(trainingData_y[idx])

print(len(real_y))

x_train,x_val,y_train,y_val = train_test_split(trainingData_x,real_y,test_size = 0.25)
print(len(x_train))
print(len(y_train))
print(len(x_val))
print(len(y_val))
print(x_train[-1])
print(y_train[-1])

estimators = KMeans(n_clusters=4)

fignum = 1

fig = plt.figure(fignum, figsize=(4, 3))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

estimators.fit(x_train)
labels = estimators.labels_

print(x_train[:, 3])
       
ax.scatter(x_train[:, 3], x_train[:, 0], x_train[:, 2], c=labels.astype(np.float), edgecolor='k')

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title(titles[fignum - 1])
ax.dist = 12

# Plot the ground truth
fig = plt.figure(fignum, figsize=(4, 3))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(x_train[y == label, 3].mean(),
              x_train[y == label, 0].mean(),
              x_train[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
y = np.choose(y, [1, 2, 0]).astype(np.float)
ax.scatter(x_train[:, 3], x_train[:, 0], x_train[:, 2], c=y, edgecolor='k')

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('Ground Truth')
ax.dist = 12

fig.show()