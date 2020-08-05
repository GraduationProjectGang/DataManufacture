import numpy as np
import random
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
import csv
import ast


from federated_method import *
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


filePath_data = 'trainingData2.csv'
filePath_stress = 'stressData2.csv'

trainingData_x = []
trainingData_y = []

with open(filePath_data, encoding='UTF-8') as file:
    data = csv.reader(file)

    for object in data:
        dummy_list = []
        for each in object:
            each = ast.literal_eval(each)
            map(float, each)
            dummy_list.append(each)

        trainingData_x.append(dummy_list)

with open(filePath_stress, encoding='UTF-8') as file:
    data = csv.reader(file)
    for listt in data:
        for stressCount in listt:
            trainingData_y.append(float(stressCount))

trainingData_x = np.array(trainingData_x)

trainingData_x = ((2 * (trainingData_x - trainingData_x.min(axis=0))) / (
            trainingData_x.max(axis=0) - trainingData_x.min(axis=0))) - 1
trainingData_x = np.reshape(trainingData_x, (4014, 5, 6))

# # declear path to your mnist data folder
# img_path = '/path/to/your/training/dataset'
#
# # get the path list using the path object
# image_paths = list(paths.list_images(img_path))
#
# # apply our function
# image_list, label_list = load(image_paths, verbose=10000)

# binarize the labels
lb = LabelBinarizer()
# label_list = lb.fit_transform(label_list)
trainingData_y = lb.fit_transform(trainingData_y)
# split data into training and test set
X_train, X_test, y_train, y_test = train_test_split(trainingData_x,
                                                    trainingData_y,
                                                    test_size=0.9,
                                                    random_state=42)

# create clients
clients = create_clients(X_train, y_train, num_clients = 10, initial='client')

# process and batch the training data for each client
clients_batched = dict()
for (client_name, data) in clients.items():
    clients_batched[client_name] = batch_data(data)

# process and batch the test set
test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))

comms_round = 100

# create optimizer
lr = 0.01
loss = 'categorical_crossentropy'
metrics = ['accuracy']
optimizer = Adam(lr=lr,
                decay=lr / comms_round,
                )

# initialize global model
smlp_global = SimpleMLP()
global_model = smlp_global.build(X_train.shape, 4)

# commence global training loop
for comm_round in range(comms_round):

    # get the global model's weights - will serve as the initial weights for all local models
    global_weights = global_model.get_weights()

    # initial list to collect local model weights after scalling
    scaled_local_weight_list =[]

    # randomize client data - using keys
    client_names = list(clients_batched.keys())
    random.shuffle(client_names)

    # loop through each client and create new local model
    for client in client_names:
        smlp_local = SimpleMLP()
        local_model = smlp_local.build(None, 4)
        local_model.compile(loss=loss,
                            optimizer=optimizer,
                            metrics=metrics)

        # set local model weight to the weight of the global model
        local_model.set_weights(global_weights)

        # fit local model with client's data
        local_model.fit(clients_batched[client], epochs=1, verbose=0)

        # scale the model weights and add to list
        scaling_factor = weight_scalling_factor(clients_batched, client)
        scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
        scaled_local_weight_list.append(scaled_weights)

        # clear session to free memory after each communication round
        K.clear_session()

    # to get the average over all the local model, we simply take the sum of the scaled weights
    average_weights = sum_scaled_weights(scaled_local_weight_list)

    # update global model
    global_model.set_weights(average_weights)

    # test global model and print out metrics after each communications round
    for (X_test, Y_test) in test_batched:
        global_acc, global_loss = test_model(X_test, Y_test, global_model, comm_round)
        SGD_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(len(y_train)).batch(320)
smlp_SGD = SimpleMLP()
SGD_model = smlp_SGD.build(None, 4)

SGD_model.compile(loss=loss,
                  optimizer=optimizer,
                  metrics=metrics)

# fit the SGD training data to model
_ = SGD_model.fit(SGD_dataset, epochs=100, verbose=0)

# test the SGD global model and print out metrics
for (X_test, Y_test) in test_batched:
    SGD_acc, SGD_loss = test_model(X_test, Y_test, SGD_model, 1)