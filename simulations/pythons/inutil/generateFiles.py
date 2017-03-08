#this file processes the data obtained in a simulation
import subprocess,os, imp

#generate the nod.xml and edge.xml files (for in case they are not given)
subprocess.call(["netconvert", "--sumo-net-file", "input/mapa.net.xml", "--plain-output", "netDef/xml/mapa"])
#this command generates four files: mapa.nod.xml, mapa.edg.xml, mapa.tll.xml, mapa.edg.xml

#convert the xml files into csv
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
subprocess.call(["Rscript", "postprocess/codis/generateFdat.R"])

subprocess.call(["Rscript", "postprocess/codis/generateCdat.R"])

