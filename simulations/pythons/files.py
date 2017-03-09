import subprocess, os, imp
#generates de configuration file
def configuration(t):
	with open("configuration.sumocfg", 'w') as doc:	
		print >> doc, '''<configuration>
	<input>
		<net-file value="input/mapa.net.xml"/>
		<route-files value="input/rutes.rou.xml"/>>
		<additional-files value="input/additional.add.xml"/>
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
	#generate the nod.xml and edge.xml files (for in case they are not given)
	subprocess.call(["netconvert", "--sumo-net-file", "input/mapa.net.xml", "--plain-output", "netDef/xml/mapa"])
	#this command generates four files: mapa.nod.xml, mapa.edg.xml, mapa.tll.xml, mapa.edg.xml

	#convert the xml files into csv
	os.system("$SUMO_HOME/tools/xml/xml2csv.py netDef/xml/mapa.edg.xml -o netDef/csv/edges.csv")
	os.system("$SUMO_HOME/tools/xml/xml2csv.py netDef/xml/mapa.nod.xml -o netDef/csv/nodes.csv")
	os.system("$SUMO_HOME/tools/xml/xml2csv.py netDef/xml/mapa.tll.xml -o netDef/csv/mapa.tll.csv")

	#generate the J.dat file
	modl = imp.load_source('generateJdat','postprocess/codes/generateJdat.py')
	import generateJdat
	generateJdat

	#generates the E.dat file
	modl = imp.load_source('generateEdgeFiles','postprocess/codes/generateEdgeFiles.py')
	import generateEdgeFiles
	generateEdgeFiles
	
	#generates the C.dat file
	subprocess.call(["Rscript", "postprocess/codes/generateCdat.R"])

#generates the additional file
def additional(maxDur, frequency):
    C = eval(open("postprocess/data/C.dat").read())
    E = eval(open("postprocess/data/E.dat").read())
    J = eval(open("postprocess/data/J.dat").read())
    with open("input/additional.add.xml", 'w') as doc:
        doc.write("<additional>\n")       
        #sets the detectors, one for every lane 
        path = os.getcwd()
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

