#we write the J.dat file that contains information about wich edges 
#are controlled by a single traffic ligths (junction)
#junctions are defined in the nodes.csv file
import csv
import os

edgesfile = open("simulations/netDef/csv/edges.csv", 'r')
#relevant columns: 1: edge from, 3: edge to, 6: edge ID
nodesfile = open("simulations/netDef/csv/nodes.csv", 'r')
#relevant columns: 7: traffic light ID, 8: junction type,  9 : node ID 

ereader = csv.reader(edgesfile, delimiter = ";")
nreader = csv.reader(nodesfile, delimiter = ";")

#we create a dictionary to know which junctions are traffic ligths
jtype = {}
namesNodes = next(nreader)
posJid = namesNodes.index('node_id')
posJtype = namesNodes.index('node_type')	
next(nreader)
for row in nreader:
	jtype[str(row[posJid])] = row[posJtype]

#we create a dictionary with the edges regulated by every junction
regulated = {}
namesEdges = next(ereader)
posTo = namesEdges.index('edge_to')
posEid = namesEdges.index('edge_id')
for row in ereader:
	j = str(row[posTo])
	if jtype[j] == "traffic_light":
		if regulated.has_key(j) :
			regulated[j].append(row[posEid])
		else:
			regulated[j] = [row[posEid]] 

def getEdges(n):
	ls = regulated[str(n)]
	s = ' '.join(ls)
	return s

datfile = open("simulations/postprocess/data/J.dat", 'w')
datfile.write("{\n")
s = "\t{idx}:{{'JunctionID' : '{name}', 'index' : {idx}, 'edges' : {edgesList}, 'numEdges' : {num}}}"
nodes = regulated.keys()
idx = 0
for node in nodes[:-1]:	#all of them except the last
	datfile.write(s.format(name = node, idx = idx, edgesList = regulated[node], num = len(regulated[node])))
	datfile.write(",\n")
	idx = idx + 1
#the last
datfile.write(s.format(name = nodes[-1], idx = idx, edgesList = regulated[nodes[-1]], num = len(regulated[nodes[-1]])))
datfile.write("\n}")

datfile.close()
edgesfile.close()
nodesfile.close()
