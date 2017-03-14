import time, os, subprocess, csv
start_time = time.time()
#network parameters:
n = 5           #size of the grid
nlanes = 3      #number of lanes
l = 150         #lenght of a street
frequency = 60  #frequency of the detectors

ncases = 8      #number of scenarios (including case0)

seed_train = 10
seed_test = 20

t_train = 8*3600
t_test = 4*3600

#generates the network
from simulations.pythons import network as nw
nw.generate(n,l,nlanes)

from simulations.pythons import simulate
maxDurs = range(10,61,5)
simulate.train(t_train, seed_train, maxDurs, frequency, ncases)

print '-------- Generating action list --------'
#obtain the action list (creates output/actionList.txt) and take the best value for case0
maxDur = subprocess.check_output(["Rscript", "analysis/actionlist.R", str(ncases)], universal_newlines=True)
maxDur = int(maxDur)
print 'Done\n'

simulate.test(t_test, seed_test, maxDur, frequency, ncases)

os.system('rm -r output/xml/')
os.system('rm configuration.sumocfg')

print 'Total time of execution: {} seconds'.format(str(time.time()-start_time))
