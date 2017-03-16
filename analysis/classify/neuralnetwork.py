import numpy as np
import time
from keras.utils import np_utils
ncases = 8
def clean(data, ncases):
	X = np.delete(data, 0, 0)
	(rows, cols) = X.shape
	Y = X[:,cols-1]
	Y = np_utils.to_categorical(Y, ncases)
	X = np.delete(X, cols-1,1)
	X = X.astype('float32')
	return (X,Y) 

#train data
data = np.genfromtxt('output/train/train.csv', delimiter = ';')
(X_train,Y_train) = clean(data, ncases)

#test data
data = np.genfromtxt('output/test/test.csv', delimiter = ';')
(X_test, Y_test) = clean(data, ncases)
del data

#neural network using keras
from keras.models import Sequential
from keras.layers import Dense, Activation
(rows, cols) = X_train.shape

#define the network
np.random.seed(1000)
model = Sequential()
model.add(Dense(128, activation = 'relu', input_shape = (cols,)))
model.add(Dense(ncases, activation = 'softmax'))

model.summary()

#define the optimizer
from keras.optimizers import SGD
lr = 0.01
decay = 0
optim = SGD(lr = lr, decay = decay, momentum = 0.9, nesterov = True)
model.compile(loss='categorical_crossentropy', 
	optimizer = optim, 
	metrics = ['accuracy'])

#train the network and evaluation
batch_size = 10
nb_epoch = 2
verbose = 2
t = time.time()
history = model.fit(X_train, Y_train, 
	batch_size = batch_size,
	epochs = nb_epoch,
	verbose = verbose,
	validation_data = (X_test,Y_test))

print(time.time() - t, 'seconds')
import matplotlib.pyplot as plt  
from utils import plot_curves
plot_curves(history, nb_epoch)
