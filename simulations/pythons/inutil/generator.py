#this script creates the network definition (nod.xml, edg.xml) and the net.xml. 
#it also creates the trips file (trips.xml), the routes file (rou.xml), the
#configuration file (.sumocfg) and the additional files (defining the detectors)
def generator(n,l,t, frequency):
	import subprocess, imp, os

	path = os.getcwd() #ends without /

	modl = imp.load_source('networkgenerator', path + '/simGen/networkgenerator.py')
	import networkgenerator
	modl = imp.load_source('tripsGenerator', path + '/simGen/tripsGenerator.py')
	import tripsGenerator
	
	modl = imp.load_source('generateFiles', path + '/pythons/generateFiles.py')	
	import generateFiles	

	#generates the network
	networkgenerator.networkgenerator(l,n)

	#generates the traffic
	tripsGenerator.writeTrips(0,t)

	#rutes file
	subprocess.call(["duarouter", "-v", "-n", "input/mapa.net.xml", "-t", "input/trips.trips.xml", "-o", "input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])

	#generates the necessary files (C.dat, F.dat, E.dat ...)
	generateFiles
	
	E = eval(open("postprocess/data/E.dat").read())
	#sets the detectors
	with open("input/additional.add.xml", 'w') as doc:
		doc.write("<additional>\n")
		#we build a detector for every lane 
		path = os.getcwd()
		s = '\t<inductionLoop id="{name}" lane="{name}" pos="10" freq="{freq}" file="' + path + '/output/xml/detectors.xml"/>\n'
		for e in E:
	    		for i in range(E[e]['numLanes']):
				doc.write(s.format(name = E[e]['edgeID'] + "_" + str(i), freq = frequency))
		doc.write("</additional>")

	#generates de configuration file
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

