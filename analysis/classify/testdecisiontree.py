#decision tree
from sklearn import tree
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

depths = [4, 6, 8, 10, 12, 14, 16, 18, 20]
min_samples_splits = range(2,51)
min_samples_leafs = [1, 5, 10, 15, 20]
criterion = 'entropy'
best_acc = 0
for min_samples_leaf in min_samples_leafs:
	doc = open('analysis/models/testtrees' + str(min_samples_leaf) + '.csv', 'w')
	doc.write('min_split;depth;accuracy_train;accuracy_test\n')
	print('------ min_samples_leaf: ' + str(min_samples_leaf) + ' --------')
	for min_samples_split in min_samples_splits:
		for depth in depths:
			print('		depth: ' + str(depth) + '	samples_split: ' + str(min_samples_split))
			model = tree.DecisionTreeClassifier(
				criterion = criterion,
				max_depth = depth,
				min_samples_split = min_samples_split,
				min_samples_leaf = min_samples_leaf
			)
			model = model.fit(X_train, Y_train)

			#test the model
			from sklearn.metrics import accuracy_score, log_loss
			Y_pred = model.predict(X_train)
			accuracy_train = accuracy_score(Y_train, Y_pred)
		
			Y_pred = model.predict(X_test)
			accuracy_test = accuracy_score(Y_test, Y_pred)
		
			doc.write(str(min_samples_split) + ';' + str(depth) + ';' + str(accuracy_train) + ';' + str(accuracy_test) + '\n')
			if (accuracy_test > best_acc):
				best_acc = accuracy_test
				opt_split = min_samples_split
				opt_depth = depth
				opt_leaf = min_samples_leaf
			
	doc.close()

print('Best tree:')
print('split: ' + str(opt_split) + '	depth: ' + str(opt_depth) + '	leaf: ' + str(opt_leaf) + '	accuracy: ' + str(best_acc))
