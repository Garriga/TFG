def generate(l,n,nlanes): 
    from simGen import networkgenerator, tripsGenerator
    from pythons import files
    from pythons import auxiliary
    
    aux.check('netDef/')
    aux.check('netDef/csv/')
    aux.check('netDef/xml/')
    aux.check('input/')

    #generates the network
    networkgenerator.networkgenerator(l,n, nlanes)

    #generates the necessary files (C.dat, J.dat, E.dat ...)
    aux.check('postprocess/data/')
    files.dat()
