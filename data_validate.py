import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils

loaded_model = keras.models.load_model('C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\best_model.h5')

# trainingData_x = (trainingData_x - trainingData_x.min(axis=0)) / (trainingData_x.max(axis=0) - trainingData_x.min(axis=0))

input = [[[0. ,        0.   ,      0.     ,    0.     ,    0.        ],
    [0.    ,     0.     ,    0.      ,   0.35714286, 0.14893001],
    [0.    ,     0.     ,    0.    ,     0.5    ,    0.01761471],
    [0.    ,     0.    ,     0.    ,     0.14285714, 0.01098109],
    [0.    ,     0.    ,     0.     ,    0.21428571, 0.03756304]]]

output = 2.0

input = np.array(input)

pred_out = loaded_model.predict(input)
print(pred_out)
