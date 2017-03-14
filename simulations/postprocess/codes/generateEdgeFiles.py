import csv

edgelist = open("simulations/netDef/csv/edges.csv", 'r')

datfile = open("simulations/postprocess/data/E.dat", 'w')
reader = csv.reader(edgelist, delimiter = ';')
datfile.write("{\n")

namesEdges = next(reader)
posEid = namesEdges.index('edge_id')
posNumLanes = namesEdges.index('edge_numLanes')
	
s = "\t{idx}:{{'edgeID' : '{name}', 'index' : {idx}, 'numLanes' : {numL}}}"
idx = 0
#we have to do a line manually to get correctly the comas configuration 
#int the .dat file
row = next(reader)
#write file
datfile.write(s.format(idx = str(idx), name = row[posEid], numL = str(row[posNumLanes])))
idx = idx + 1
for row in reader:
	#write file
	datfile.write(",\n")
	datfile.write(s.format(idx = str(idx), name = row[posEid], numL = str(row[posNumLanes])))
	idx = idx + 1
datfile.write("\n}")	
edgelist.close()
datfile.close()

