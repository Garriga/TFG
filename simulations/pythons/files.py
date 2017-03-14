import subprocess, imp, os
#generates de configuration file
def configuration(t):
	with open("configuration.sumocfg", 'w') as doc:	
		print >> doc, '''<configuration>
	<input>
		<net-file value="simulations/input/mapa.net.xml"/>
		<route-files value="simulations/input/rutes.rou.xml"/>>
		<additional-files value="simulations/input/additional.add.xml"/>
	</input>	
	<output>
		<tripinfo-output value="output/xml/tripinfo.xml"/>
	</output>
	<time>
		<begin value="0"/>
		<end value="{}"/>
	</time>
</configuration>
'''.format(str(t))

#this file generates the data given a nod.xml file (a network)
def dat():
    path = os.getcwd()	
    #generate the nod.xml and edge.xml files (for in case they are not given)
    subprocess.call(["netconvert", "--sumo-net-file", "simulations/input/mapa.net.xml", "--plain-output", "simulations/netDef/xml/mapa"])
	#this command generates four files: mapa.nod.xml, mapa.edg.xml, mapa.tll.xml, mapa.edg.xml

	#convert the xml files into csv
    os.system("$SUMO_HOME/tools/xml/xml2csv.py simulations/netDef/xml/mapa.edg.xml -o simulations/netDef/csv/edges.csv")
    os.system("$SUMO_HOME/tools/xml/xml2csv.py simulations/netDef/xml/mapa.nod.xml -o simulations/netDef/csv/nodes.csv")
    os.system("$SUMO_HOME/tools/xml/xml2csv.py simulations/netDef/xml/mapa.tll.xml -o simulations/netDef/csv/mapa.tll.csv")

	#generate the J.dat file
    modl = imp.load_source('generateJdat', path + '/simulations/postprocess/codes/generateJdat.py')
    import generateJdat
    generateJdat

	#generates the E.dat file
    modl = imp.load_source('generateEdgeFiles', path + '/simulations/postprocess/codes/generateEdgeFiles.py')
    import generateEdgeFiles
    generateEdgeFiles

	#generates the C.dat file
    subprocess.call(["Rscript", path + "/simulations/postprocess/codes/generateCdat.R"])

#generates the additional file
def additional(maxDur, frequency):
    path = os.getcwd()
    C = eval(open("simulations/postprocess/data/C.dat").read())
    E = eval(open("simulations/postprocess/data/E.dat").read())
    J = eval(open("simulations/postprocess/data/J.dat").read())
    with open("simulations/input/additional.add.xml", 'w') as doc:
        doc.write("<additional>\n")       
        #sets the detectors, one for every lane 
        inductionLoop = '\t<inductionLoop id="{name}" lane="{name}" pos="10" freq="{freq}" file="' + path + '/output/xml/detectors.xml"/>\n'
        for e in E:
            for i in range(E[e]['numLanes']):
                doc.write(inductionLoop.format(name = E[e]['edgeID'] + "_" + str(i), freq = frequency))
        #TLS configuration		
        #auxiliar function    	
        def generateState(x, n):
            state = ["r"]*n
            for i in x:
                state[i] = "G"
            return("".join(state))
        
        tls = '\t<tlLogic id="{name}" programID="Program{name}" offset="0" type="actuated">\n'
		#phase = '\t\t<phase duration="{dur}" minDur="5" maxDur="{maxDuration}" state="{st}"/>'
        phase = '\t\t<phase duration="60" minDur="5" maxDur="{maxDuration}" state="{st}"/>\n'
        phaseyellow = '\t\t<phase duration="4" state="{}"/>\n'
		
        #we construct a dictionary to know the number of every edge
        getLinks = {}
        getNum = {}	
        for c in C:
            getLinks[C[c]['edge']] = C[c]['links']
            getNum[C[c]['edge']] = C[c]['numLinks']
	
        for j in J:
            doc.write(tls.format(name = J[j]['JunctionID']))
            #one phase for every edge regulated by the street
            for  e in J[j]['edges']:
                state = generateState(getLinks[e], getNum[e])
		        #doc.write(phase.format(dur = duration, maxDuration = maxDur, st = state))
                doc.write(phase.format(maxDuration = maxDur, st = state))   
                #set the green values to yellow
                state = state.replace("G", "y")
                doc.write(phaseyellow.format(state))
            doc.write("\t</tlLogic>\n")
        doc.write("</additional>")

