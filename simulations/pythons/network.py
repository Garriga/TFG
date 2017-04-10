from simulations.simGen import networkgenerator
from simulations.pythons import files
from simulations.pythons import auxiliary as aux

def generate(n,l,nlanes):   
    aux.check('simulations/netDef/')
    aux.check('simulations/netDef/csv/')
    aux.check('simulations/netDef/xml/')
    aux.check('simulations/input/')

    #generates the network
    networkgenerator.networkgenerator(l,n, nlanes)
	#generates the necessary files (C.dat, J.dat, E.dat ...)
    aux.check('simulations/postprocess/data/')
    files.dat()
