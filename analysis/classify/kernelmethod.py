import numpy as np
np.random.seed(1000)
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

from sklearn import svm
from sklearn.model_selection import GridSearchCV
model = svm.SVC(
	probability = True
)
parameters = [
	{'kernel' : ['rbf'], 'gamma' : ['auto', 1e-4, 1e-3, 0.01, 0.1, 1, 2, 3], 
	'C' : [0.001, 0.01, 0.1, 1]},
	{'kernel' : ['linear'], 'C' : [0.001, 0.01, 0.1, 1]}]
model = GridSearchCV(model, parameters, verbose = 3)
model = model.fit(X_train, Y_train)
print('The best parameters obtained are:')
print(model.best_params_)
print('')

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

from sklearn.metrics import classification_report
names = ['case' + str(s) for s in range(0,ncases)]
print(classification_report(Y_test, Y_pred, target_names = names))

#save the model
from sklearn.externals import joblib
joblib.dump(model, 'analysis/models/svm.pkl')
