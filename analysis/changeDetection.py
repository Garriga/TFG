import numpy as np
import pandas as pd
from sklearn.externals import joblib

def load_data(case, seed):
	data = np.genfromtxt('output/NS/detectors/postprocess/case{}s{}.csv'.format(case, seed), delimiter = ';')
	data = np.delete(data, 0, 0)	#remove first row (detector name)
	data = data.astype('float32')
	return data

def get_time(y_pred, l):	 #pred un numpy array
	n = y_pred.shape[0]
	ref = 0		#reference case
	cont = 0
	case = 0
	for i in range(0,n):
		if (y_pred[i] != ref):
			if (y_pred[i] == case):
				cont += 1
			else:
				cont = 1
				case = y_pred[i]
		else:
			case = 0
			cont = 0
		if (cont == l):
			break
	
	t_detection = i*60
	return(t_detection, case)

def detect(case, seed, algorithm, consecutive):
	if (algorithm == 'neural_network'):
		filename = 'analysis/models/neuralnetwork.pkl'
	elif (algorithm == 'nearest_neighbour'):
		filename = 'analysis/models/nearestneighbour.pkl'
	elif (algorithm == 'kernel'):
		filename = 'analysis/models/svm.pkl'
	elif (algorithm == 'bayes'):
		filename = 'analysis/models/bayes.pkl'
	elif (algorithm == 'decision_tree'):
		filename = 'analysis/models/decisiontree.pkl'
	model = joblib.load(filename)
	data = load_data(case, seed)
	if (algorithm == 'neural_network'):
		scaler = joblib.load('analysis/models/neuralnetwork_scaler.pkl')
		data = scaler.transform(data)
	y_pred = model.predict(data)
	return(get_time(y_pred, consecutive))
