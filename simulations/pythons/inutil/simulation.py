def run():
	import subprocess, os
	#run the simulation
	sumoProcess = subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1"])
	os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/csv/tripinfo.csv")
	os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/csv/detectors.csv")
#sumopProcess = subprocess.call(["sumo", "-n", "input/mapa.net.xml", "-r", "input/rutes.rou.xml", "-a", "input/additional.add.xml", "--tripinfo-output", "tripinfo.xml"])

