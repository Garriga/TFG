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

#testing linear and RBF kernels
opt_accuracy = 0

from sklearn import svm
C = [0.001, 0.01, 0.1, 1, 10]
gammas = [1e-5, 1e-4, 1e-3, 0.01, 0.1, 1, 10]

doc = open('analysis/models/kernel_linear.csv', 'w')
doc.write('C;accuracy_train;accuracy_test\n')
print('----- Testing linear kernel -----')
for c in C:
	print('C: ' + str(c))
	model = svm.SVC(
		kernel = 'linear',
		C = c
	)
	model.fit(X_train, Y_train)

	#test the model
	from sklearn.metrics import accuracy_score, log_loss
	Y_pred = model.predict(X_train)
	accuracy_train = accuracy_score(Y_train, Y_pred)
	Y_pred = model.predict(X_test)
	accuracy_test = accuracy_score(Y_test, Y_pred)
			
	doc.write(str(c) + ';' + str(accuracy_train) + ';' + str(accuracy_test) + '\n')
	if (opt_accuracy < accuracy_test):
		opt_accuracy = accuracy_test
		opt_type = 'linear'
		opt_C = c
doc.close()

doc = open('analysis/models/kernel_rbf.csv', 'w')
doc.write('C;gamma;accuracy_train;accuracy_test\n')
print('----- Testing rbf kernel -----')
for c in C:
	for gamma in gammas:
		print('C: ' + str(c) + '	gamma: ' + str(gamma))
		model = svm.SVC(
			kernel = 'rbf',
			C = c,
			gamma = gamma
		)
		model.fit(X_train, Y_train)
				
		#test the model
		from sklearn.metrics import accuracy_score, log_loss
		Y_pred = model.predict(X_train)
		accuracy_train = accuracy_score(Y_train, Y_pred)
		Y_pred = model.predict(X_test)
		accuracy_test = accuracy_score(Y_test, Y_pred)
		doc.write(str(c) + ';' + str(gamma) + ';' + str(accuracy_train) + ';' + str(accuracy_test) + '\n')
		if (opt_accuracy < accuracy_test):
			opt_accuracy = accuracy_test
			opt_type = 'rbf'
			opt_C = c
			opt_gamma = gamma

doc.close()

if (opt_type == 'linear'):
	print('linear C: ' + str(opt_C))
else:
	print('rbf C: ' + str(opt_C) + ' gamma: ' + str(opt_gamma))
