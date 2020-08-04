import tensorflow as tf
import numpy as np
import random
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
import keras
import ast
from ast import literal_eval
from keras.layers import Dense, Embedding, LSTM, Dropout
from keras.layers import Flatten
import csv
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Activation
from keras.utils import np_utils
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

class FL_LSTM:
    @staticmethod
    def build(one_hot_vec_size):
        model = Sequential()
        model.add(LSTM(128, stateful=True, input_shape=x_train.shape, batch_input_shape=(1,5,6)))
        model.add(Dropout(0.5))
        model.add(Dense(one_hot_vec_size, activation='softmax'))
        return model
    
def weight_scalling_factor(clients_trn_data, client_name):
    client_names = list(clients_trn_data.keys())
    #get the bs
    bs = list(clients_trn_data[client_name])[0][0].shape[0]
    print(bs)
    #first calculate the total training data points across clinets
    global_count = sum([tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy() for client_name in client_names])*bs
    # get the total number of data points held by a client
    local_count = tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy()*bs
    return local_count/global_count


def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final



def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)
        
    return avg_grad


def test_model(X_test, Y_test,  model, comm_round):
    cce = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    #logits = model.predict(X_test, batch_size=100)

    X_test = np.array(X_test)

    logits = model.predict(X_test)
    loss = cce(Y_test, logits)
    acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
    print('comm_round: {} | global_acc: {:.117%} | global_loss: {}'.format(comm_round, acc, loss))
    return acc, loss

filePath_data = 'C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\trainingData2.csv'
filePath_stress = 'C:\\Users\\Team6\\Documents\\GitHub\\DataManufacture\\stressData2.csv'

trainingData_x = []
trainingData_y = []

def create_clients(vector_list, label_list, num_clients=10, initial='clients'):
    ''' return: a dictionary with keys clients' names and value as 
                data shards - tuple of images and label lists.
        args: 
            image_list: a list of numpy arrays of training images
            label_list:a list of binarized labels for each image
            num_client: number of fedrated members (clients)
            initials: the clients'name prefix, e.g, clients_1 
    '''
    #create a list of client names
    client_names = ['{}_{}'.format(initial, i+1) for i in range(num_clients)]

    #randomize the data
    data = list(zip(vector_list, label_list))
    random.shuffle(data)

    #shard data and place at each client
    size = len(data)//num_clients
    shards = [data[i:i + size] for i in range(0, size*num_clients, size)]

    #number of clients must equal number of shards
    assert(len(shards) == len(client_names))

    return {client_names[i] : shards[i] for i in range(len(client_names))}

def batch_data(data_shard, bs=1):
    '''Takes in a clients data shard and create a tfds object off it
    args:
        shard: a data, label constituting a client's data shard
        bs:batch size
    return:
        tfds object'''
    #seperate shard into data and labels lists
    data, label = zip(*data_shard)
    dataset = tf.data.Dataset.from_tensor_slices((list(data), list(label)))
    return dataset.shuffle(len(label)).batch(bs)

with open(filePath_data, encoding= 'UTF-8') as file:
       data = csv.reader(file)

       for object in data:
              dummy_list = []
              for each in object:
                     each = ast.literal_eval(each)
                     map(float, each)
                     dummy_list.append(each)

              trainingData_x.append(dummy_list)

with open(filePath_stress, encoding= 'UTF-8') as file:
       data = csv.reader(file)
       for list_ in data:
              for stressCount in list_:
                     trainingData_y.append(float(stressCount))

trainingData_x = np.array(trainingData_x)

trainingData_x = ((2 * (trainingData_x - trainingData_x.min(axis=0))) / (trainingData_x.max(axis=0) - trainingData_x.min(axis=0))) - 1
trainingData_x = np.reshape(trainingData_x, (4014, 5, 6))

x_train,x_val,y_train,y_val = train_test_split(trainingData_x, trainingData_y, test_size = 0.1)

y_train = np_utils.to_categorical(y_train)
y_val = np_utils.to_categorical(y_val)
one_hot_vec_size = y_train.shape[1]
print(y_train.shape[0], " ", y_train.shape[1], " ", y_train.shape, " ", one_hot_vec_size)

print(x_train.shape)

clients = create_clients(x_train, y_train, num_clients=10, initial='client')

clients_batched = dict()
for (client_name, data) in clients.items():
    clients_batched[client_name] = batch_data(data)

test_batched = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(len(y_val))

smlp_global = FL_LSTM()
global_model = smlp_global.build(one_hot_vec_size)
global_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

comms_round = 100
lr = 0.01
#commence global training loop
for comm_round in range(comms_round):

    # get the global model's weights - will serve as the initial weights for all local models
    global_weights = global_model.get_weights()
    
    #initial list to collect local model weights after scalling
    scaled_local_weight_list = list()

    #randomize client data - using keys
    client_names= list(clients_batched.keys())
    random.shuffle(client_names)
    
    #loop through each client and create new local model
    for client in client_names:
        smlp_local = FL_LSTM()
        local_model = smlp_local.build(one_hot_vec_size)
        local_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        #set local model weight to the weight of the global model
        local_model.set_weights(global_weights)
        
        #fit local model with client's data
        local_model.fit(clients_batched[client], epochs=1, verbose=0)
        
        #scale the model weights and add to list
        scaling_factor = weight_scalling_factor(clients_batched, client)
        scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
        scaled_local_weight_list.append(scaled_weights)
        
        #clear session to free memory after each communication round
        K.clear_session()
        
    #to get the average over all the local model, we simply take the sum of the scaled weights
    average_weights = sum_scaled_weights(scaled_local_weight_list)
    
    #update global model
    global_model.set_weights(average_weights)

    print(test_batched)

    #test global model and print out metrics after each communications round
    for(X_test, Y_test) in test_batched:
        global_acc, global_loss = test_model(X_test, Y_test, global_model, comm_round)
        SGD_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuff(len(y_train)).bleatch(1)

smlp_SGD = FL_LSTM()
SGD_model = smlp_SGD.build(one_hot_vec_size)

# optimizer = SGD(lr=lr, decay=lr / comms_round, momentum=0.9) 

SGD_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the SGD training data to model
_ = SGD_model.fit(SGD_dataset, epochs=100, verbose=0)

#test the SGD global model and print out metrics
for(X_test, Y_test) in test_batched:
    SGD_acc, SGD_loss = test_model(X_test, Y_test, SGD_model, 1)