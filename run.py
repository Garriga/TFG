import time, os
start_time = time.time()
#network parameters:
n = 5           #size of the grid
nlanes = 3      #number of lanes
l = 150         #lenght of a street
frequency = 60  #frequency of the detectors

ncases = 8      #number of scenarios (including case0)

seed_train = 10
seed_test = 20

#t_train = 10*3600
#t_test = 5*3600

t_test = 100
t_train = 100

#generates the network
from simulations.pythons import network as nw
nw.generate(n,l,nlanes)

from simulations.pythons import simulate
maxDurs = range(10,61,25)
simulate.train(t_train, seed_train, maxDurs, frequency, ncases)

#obtain the maxDur value used
maxDur = 16

simulate.test(t_test, seed_test, maxDur, frequency, ncases)

os.system('rm -r output/xml/')

print '\nTotal time of execution: {} seconds'.format(str(time.time()-start_time))
