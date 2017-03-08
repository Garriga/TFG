def run(t):

	import subprocess, os
	#we need to read the E, J and C files
	C = eval(open("postprocess/data/C.dat").read())
	E = eval(open("postprocess/data/E.dat").read())
	J = eval(open("postprocess/data/J.dat").read())

	def generateState(x, n):
		state = ["r"]*n
		for i in x:
		    state[i] = "G"
		return("".join(state))

	with open("input/actuated.add.xml", 'w') as actuated:
		actuated.write("<additional>\n")
		#we build a detector for every lane 
		path = os.getcwd()
		s = '\t<inductionLoop id="{name}" lane="{name}" pos="10" freq="60" file="' + path + '/output/xml/detAct.xml"/>\n'
		for e in E:
		    for i in range(E[e]['numLanes']):
			actuated.write(s.format(name = E[e]['edgeID'] + "_" + str(i)))

		#we build the traffic light programs
		s = '\t<tlLogic id="{name}" programID="Program{name}" offset="0" type="actuated">'
		phase = '\t\t<phase duration="{dur}" minDur="5" maxDur="50" state="{st}"/>'
		phasey = '\t\t<phase duration="4" state="{}"/>'
		#we construct a dictionary to know the number of every edge
		getLinks = {}
		getNum = {}	
		for c in C:
		    getLinks[C[c]['edge']] = C[c]['links']
		    getNum[C[c]['edge']] = C[c]['numLinks']
	
		for j in J:
		    #only for junctions with a traffic light
		    #WE ASSUME EVERY JUNCTION IN J CONTAINS A TRAFFIC LIGHT
		    
		    #WE NEED THE IDX FROM THE ORIGINAL EDGE FILE, NOT THE C.DAT FILE
		    actuated.write(s.format(name = J[j]['JunctionID']))
		    actuated.write('\t\t<param key="show-detectors" value="false"/>\n')
		    	    #one phase for every edge regulated by the street
		    for  e in J[j]['edges']:
			duration = 30	
			state = generateState(getLinks[e], getNum[e])
		        actuated.write(phase.format(dur = duration, st = state))
			#set the green values to yellow
			state = state.replace("G", "y")
			actuated.write(phasey.format(state))


		    actuated.write("</tlLogic>")
	 	actuated.write("</additional>")


	with open("configurationAct.sumocfg", 'w') as doc:	
		print >> doc, '''<configuration>
	<input>
		<net-file value="input/mapa.net.xml"/>
		<route-files value="input/rutes.rou.xml"/>>
		<additional-files value="input/actuated.add.xml"/>
	</input>	
	<output>
		<tripinfo-output value="output/xml/tripinfoAct.xml"/>
	</output>
	<time>
		<begin value="0"/>
		<end value="{}"/>
	</time>
</configuration>
'''.format(str(t))

	#run the simulation
	sumoProcess = subprocess.call(["sumo", "-c", "configurationAct.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1"])
	os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfoAct.xml -o output/csv/tripinfoAct.csv")
	os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detAct.xml -o output/csv/detAct.csv")

