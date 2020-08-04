import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils

loaded_model = keras.models.load_model('C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\best_model_2.h5')

# trainingData_x = (trainingData_x - trainingData_x.min(axis=0)) / (trainingData_x.max(axis=0) - trainingData_x.min(axis=0))

input = [[[0. ,        1.   ,      3.     ,    0.     ,    0.        ],
    [0.    ,     1.     ,    3.      ,   0., 0.],
    [0.    ,     1.     ,    3.    ,     0    ,    0.],
    [0.    ,     1.    ,     3.    ,     0., 0.],
    [0.    ,     1.    ,     0.     ,    0., 0.]]]

input = [[[0, 1, 3, 1.8550337827306764, 0, 0],
    [0, 1, 3, 1.8550337827306764, 0, 0],
    [0, 1, 3, 1.8550337827306764, 14, 749915],
    [0, 1, 3, 1.8550337827306764, 5, 2644291],
    [0, 1, 3, 1.8550337827306764, 7, 75112]]]

output = 2.0

input = np.array(input)

pred_out = loaded_model.predict(input)
print(pred_out)
