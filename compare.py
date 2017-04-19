from __future__ import division
import time, os, subprocess, csv
start_time = time.time()
#network parameters:
n = 5           #size of the grid
nlanes = 3      #number of lanes
l = 150         #lenght of a street
frequency = 60  #frequency of the detectors

ncases = 8      #number of scenarios (including case0)

seed_test = 20
t_test = 4*3600

#generates the network
#from simulations.pythons import network as nw
#nw.generate(n,l,nlanes)

#from simulations.pythons import simulate
#import pandas as pd
#actionList = pd.read_table('output/actionList.txt', sep = ' ')
from analysis import changeDetection

algorithms = ['neural_network', 'nearest_neighbour', 'kernel', 'bayes', 'decision_tree']
seeds = range(20,111,10)

for algorithm in algorithms:
	doc = open('output/NS/detection/detectionTimes_' + algorithm + '.csv', 'w')	
	doc.write('case;seed;consecutive;t_detection(s);t_detection(min);label\n')
	for seed in seeds:
		print(algorithm + '		seed: ' + str(seed))
		for case in range(1,ncases):
			for consecutive in range(1,6):
				t_detection, label = changeDetection.detect(case, seed, algorithm, consecutive)
				doc.write(str(case) + ';' + str(seed) + ';' + str(consecutive) + ';' + str(t_detection) + ';' + str(t_detection/60 - 90) + ';' + str(int(label)) + '\n')
		#maxDur1 = actionList["maxDur"][0]
		#maxDur2 = actionList["maxDur"][case]
		#simulate.changeTLS(t_detection + 30*60, t_test, seed_test, maxDur1, maxDur2, frequency, case, algorithm)
	doc.close()
#os.system('rm -r output/xml/')
#os.system('rm configuration.sumocfg')
#os.system('rm state.sbx')

print('Total time of execution: {} seconds'.format(str(time.time()-start_time)))
