def generate(l,n,nlanes): 
    from simGen import networkgenerator, tripsGenerator
    from pythons import files
    from pythons import directory
    
    directory.check('netDef/')
    directory.check('netDef/csv/')
    directory.check('netDef/xml/')
    directory.check('input/')

    #generates the network
    networkgenerator.networkgenerator(l,n, nlanes)

    #generates the necessary files (C.dat, J.dat, E.dat ...)
    directory.check('postprocess/data/')
    files.dat()
