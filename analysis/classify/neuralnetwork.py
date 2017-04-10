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
layers = [20, 10, 8]
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
	verbose = 2,
)
	
#train the model
model.fit(X_train, Y_train)

#test the model
from sklearn.metrics import accuracy_score, log_loss
Y_pred = model.predict(X_train)
Y_prob = model.predict_proba(X_train)
print('The accuracy obtained for train data is {:.4f} and the cross entropy is {:.4f}'
	.format(accuracy_score(Y_train, Y_pred), 
	log_loss(Y_train,Y_prob)))

Y_pred = model.predict(X_test)
Y_prob = model.predict_proba(X_test)
print('The accuracy obtained for test data is {:.4f} and the cross entropy is {:.4f}'
	.format(accuracy_score(Y_test, Y_pred), 
	log_loss(Y_test,Y_prob)))

from sklearn.metrics import classification_report, confusion_matrix
names = ['case' + str(s) for s in range(0,ncases)]
print(classification_report(Y_test, Y_pred, target_names = names))
print(confusion_matrix(Y_test, Y_pred))
#save the model
from sklearn.externals import joblib
joblib.dump(model, 'analysis/models/neuralnetwork.pkl')
