import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.utils import np_utils 
import keras 

code2idx = {'c4':0, 'd4':1, 'e4':2, 'f4':3, 'g4':4, 'a4':5, 'b4':6, 'c8':7, 'd8':8, 'e8':9, 'f8':10, 'g8':11, 'a8':12, 'b8':13} 
idx2code = {0:'c4', 1:'d4', 2:'e4', 3:'f4', 4:'g4', 5:'a4', 6:'b4', 7:'c8', 8:'d8', 9:'e8', 10:'f8', 11:'g8', 12:'a8', 13:'b8'}

seq = ['g8', 'e8', 'e4', 'f8', 'd8', 'd4', 'c8', 'd8', 'e8', 'f8', 'g8', 'g8', 'g4', 'g8', 'e8', 'e8', 'e8', 'f8', 'd8', 'd4',
       'c8', 'e8', 'g8', 'g8', 'e8', 'e8', 'e4', 'd8', 'd8', 'd8', 'd8', 'd8', 'e8', 'f4', 'e8', 'e8', 'e8', 'e8', 'e8', 'f8',
       'g4', 'g8', 'e8', 'e4', 'f8', 'd8', 'd4', 'c8', 'e8', 'g8', 'g8', 'e8', 'e8', 'e4'] 

def seq2dataset(seq, window_size): 
    dataset = [] 
    for i in range(len(seq)-window_size): 
        subset = seq[i:i+window_size+1]
        #print(subset)
        dataset.append([code2idx[item] for item in subset]) 
    return np.array(dataset)

dataset=seq2dataset(seq, window_size =4)

x_train = dataset[:, 0:4]
y_train = dataset[:, 4]
# print(x_train)
# print(y_train)

max_idx_value = 13

x_train = x_train / float(max_idx_value)
x_train = np.reshape(x_train, (50, 4, 1))
y_train = np_utils.to_categorical(y_train)

one_hot_vec_size = y_train.shape[1]
print(y_train.shape[0], " ", y_train.shape[1], " ", y_train.shape)
print(y_train)

model = Sequential()
model.add(LSTM(128, batch_input_shape = (1,4,1), stateful=True))
model.add(Dense(one_hot_vec_size, activation ='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(x_train)
print(y_train)

num_epochs=2000
for epoch_idx in range(num_epochs):
    print( 'epochs: {}'.format(epoch_idx))
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2, shuffle=False)
    model.reset_states()
# /// stateful=False 라면 위 fit 대신에 아래가 사용된다. 
# ///model.fit(x_train, y_train, epochs=2000, batch_size=10, verbose=2)


# // 한 스텝 예측
seq_out = ['g8','e8','e4','f8']
pred_count = 50

pred_out = model.predict(x_train)
for i in range(pred_count):
    idx = np.argmax(pred_out[i])
    seq_out.append(idx2code[idx])

seq_in = ['g8','e8','e4','f8']
seq_out = seq_in
seq_in = [code2idx[it] / float(max_idx_value) for it in seq_in]

# // 곡 전체 예측
for i in range(pred_count):
    sample_in = np.array(seq_in)
    sample_in = np.reshape(sample_in, (1,4,1))
    pred_out = model.predict(sample_in)
    idx = np.argmax(pred_out)
    seq_out.append(idx2code[idx])
    seq_in.append(idx / float(max_idx_value))
    seq_in.pop(0)   