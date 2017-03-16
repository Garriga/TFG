import numpy as np
import time
ncases = 8
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

#define the method
from sklearn import neighbors as nb
n = 15
model = nb.KNeighborsClassifier(n_neighbors = n, weights = 'uniform', 
	algorithm = 'auto', metric = 'minkowski')

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
