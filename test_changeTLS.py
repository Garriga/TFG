#test change in TLS
n = 5           #size of the grid
nlanes = 3      #number of lanes
l = 150         #lenght of a street
frequency = 60  #frequency of the detectors
#generates the network
from simulations.pythons import network as nw
nw.generate(n,l,nlanes)

from simulations.pythons import simulate
import pandas as pd
actionList = pd.read_table('output/actionList.txt', sep = ' ')


seed = 20
t_test = 4*3600
#for case in range(1,8):
for case in [7]:
	maxDur1 = actionList["maxDur"][0]
	maxDur2 = actionList["maxDur"][case]
	break_times = range(115*60, 156*60, 60)	#every minute (40 states saved)
	for time in break_times:
		print('----- Simulating case ' + str(case) + ' break time: ' + str(time) + ' -----')
		simulate.run_states(time, t_test, seed, maxDur1, maxDur2, frequency, case)
	#simulate.save_states(t_test, seed, maxDur1, frequency, case)
