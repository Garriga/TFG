#this file processes the data obtained in a simulation
import subprocess,os, imp

#generate the nod.xml and edge.xml files (for in case they are not given)
subprocess.call(["netconvert", "--sumo-net-file", "input/mapa.net.xml", "--plain-output", "netDef/xml/mapa"])
#this command generates four files: mapa.nod.xml, mapa.edg.xml, mapa.tll.xml, mapa.edg.xml

#convert the xml files into csv
os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/csv/detectors.csv")
os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/csv/tripinfo.csv")
os.system("$SUMO_HOME/tools/xml/xml2csv.py netDef/xml/mapa.edg.xml -o netDef/csv/edges.csv")
os.system("$SUMO_HOME/tools/xml/xml2csv.py netDef/xml/mapa.nod.xml -o netDef/csv/nodes.csv")
os.system("$SUMO_HOME/tools/xml/xml2csv.py netDef/xml/mapa.tll.xml -o netDef/csv/mapa.tll.csv")
os.system("$SUMO_HOME/tools/xml/xml2csv.py input/rutes.rou.xml -o output/csv/routes.csv")

#generate the J.dat file
modl = imp.load_source('generateJdat','postprocess/codis/generateJdat.py')
import generateJdat
generateJdat

#generates the E.dat file
modl = imp.load_source('generateEdgeFiles','postprocess/codis/generateEdgeFiles.py')
import generateEdgeFiles
generateEdgeFiles

#extract the flows and routes from the input routes file (generates the F.dat file)
R1 = subprocess.call(["Rscript", "postprocess/codis/generateFdat.R"])

R2 = subprocess.call(["Rscript", "postprocess/codis/generateCdat.R"])

subprocess.call(["python", "optimitzacio/Main.py", "postprocess/data", "optimitzacio/output"])

#Run the same problem with the optimized traffic lights programs

t = 2*3600
with open("configurationOpt.sumocfg", 'w') as doc:	
	print >> doc, '''<configuration>
	<input>
		<net-file value="input/mapa.net.xml"/>
		<route-files value="input/rutes.rou.xml"/>>
		<additional-files value="optimitzacio/output/solution.add.xml"/>
	</input>	
	<output>
		<tripinfo-output value="output/xml/tripinfoOpt.xml"/>
	</output>
	<time>
		<begin value="0"/>
		<end value="{}"/>
	</time>
</configuration>
'''.format(str(t))

#run the simulation
sumoProcess = subprocess.call(["sumo", "-c", "configurationOpt.sumocfg", "--xml-validation", "never"])
os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfoOpt.xml -o output/csv/tripinfoOpt.csv")
os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detOpt.xml -o output/csv/detOpt.csv")
