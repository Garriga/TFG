#network parameters:
n = 5           #size of the grid
nlanes = 3      #number of lanes
l = 150         #lenght of a street
frequency = 60  #frequency of the detectors

seed_train = 10
seed_test = 20

t_train = 10*3600
t_test = 5*3600

#generates the network
from pythons import network as nw
nw.generate(n,l,nlanes)

from python import train, test

train.simulate()

#obtenim el 
...

test.simulate()

