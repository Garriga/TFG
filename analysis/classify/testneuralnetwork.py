import numpy as np
import time
ncases = 8
np.random.seed(1000)

def clean(data, ncases):
	X = np.delete(data, 0, 0)
	(rows, cols) = X.shape
	Y = X[:,cols-1]
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

#preprocess
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#define the method
from sklearn.neural_network import MLPClassifier
neurons_hidden_1 = range(1,30)
#neurons_hidden_2 = range(1,61)
doc = open('analysis/models/hidden_layer_2.csv', 'w')
doc.write('first_layer;second_layer;accuracy_train;accuracy_test\n')
opt_accuracy = 0
for neurons1 in neurons_hidden_1:
	if (neurons1 < 3):
		lim = 3
	else:
		lim = neurons1
	for neurons2 in range(2,lim):
		print('----- neurons: ' + str(neurons1) + ' ' + str(neurons2) + ' -----')
		layers = [neurons1, neurons2]
		activation = 'relu'
		alpha = 0.001
		type_rate = 'adaptive'
		rate = 0.1
		momentum = 0.09
		max_iter = 2000
		model = MLPClassifier(
			solver = 'sgd',
			hidden_layer_sizes = layers,
			activation = activation,
			learning_rate = type_rate,
			learning_rate_init = rate,
			alpha = alpha,
			momentum = momentum,
			max_iter = max_iter,
			shuffle = True,
			#verbose = 2,
		)
	
		model.fit(X_train, Y_train)
	
		from sklearn.metrics import accuracy_score, log_loss
		Y_pred = model.predict(X_train)
		accuracy_train = accuracy_score(Y_train, Y_pred)
		Y_pred = model.predict(X_test)
		accuracy_test = accuracy_score(Y_test, Y_pred)
		doc.write(str(neurons1) + ';' + str(neurons2) + ';' + str(accuracy_train) + ';' + str(accuracy_test) + '\n')
	
		if (opt_accuracy < accuracy_test):
			opt_accuracy = accuracy_test
			opt_neurons1 = neurons1
			opt_neurons2 = neurons2
		

doc.close()

print('Optimal number of neurons: ' + str(opt_neurons1) + ' second layer: ' + 
	str(opt_neurons2)  + '  accuracy obtained: ' + str(opt_accuracy))
