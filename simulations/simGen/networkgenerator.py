import subprocess, datetime 
#creates a nodes file (.nod.xml)
def nodgenerator(l,n): 
	with open("simulations/input/nodes.nod.xml", 'w') as nodes:
		nodes.write('<nodes>\n')
		for i in range(n*n): # i = 0,1,2...n
			x = (i%n)*l			
			y = (n-1-i//n)*l	
			nodes.write('	<node id="{}" x="{}" y="{}" type="traffic_light" />\n'.format(str(i), str(x), str(y)))
		#auxiliar nodes
		for i in range(n):
			#top nodes
			nodes.write('	<node id="{}" x="{}" y="{}" />\n'.format(str(n*n+i), str(i*l), str(n*l)))
			#bottom nodes
			nodes.write('	<node id="{}" x="{}" y="{}" />\n'.format(str(n*n+n+i), str(i*l), str(-l)))
			#right nodes
			nodes.write('	<node id="{}" x="{}" y="{}" />\n'.format(str(n*n+2*n+i), str(n*l), str(i*l)))
			#left nodes
			nodes.write('	<node id="{}" x="{}" y="{}" />\n'.format(str(n*n+3*n+i), str(-l), str(i*l)))
		nodes.write('</nodes>\n')

def edgegenerator(n, nlanes):
	with open("simulations/input/edges.edg.xml", 'w') as edges:
		edges.write('<edges>\n')
		#the edges are build following rows and columns
		for i in range(n):
		#i indicates the column, j the edge in the column
			for j in range(n-1):
				origin = i%5+5*j
				destination = i%5+5*(j+1)
				# one street in each direcion
				if (i%2 == 1):
					origin, destination = destination, origin			
				edges.write('	<edge from="{orig}" id="{orig}to{dest}" to="{dest}" numLanes="{lanes}"/>\n'.format(orig=str(origin), dest=str(destination), lanes = str(nlanes)))
		#columns
		for i in range(n):
		#i indicates the row, j the edge in the row
			for j in range(n-1):
				origin = 5*i+j
				destination = 5*i+j+1
				if (i%2 == 1):
					origin, destination = destination, origin
				edges.write('	<edge from="{orig}" id="{orig}to{dest}" to="{dest}" numLanes="{lanes}" />\n'.format(orig=str(origin), dest=str(destination), lanes = str(nlanes)))
		# auxiliary edges
		for i in range(n): 
			# top			
			origin = n*n+i;
			destination = i;
			if (i%2 == 1):
				origin, destination = destination, origin 
			edges.write('	<edge from="{orig}" id="{orig}to{dest}" to="{dest}" numLanes="{lanes}"/>\n'.format(orig=str(origin), dest=str(destination), lanes = str(nlanes)))
			# bottom
			origin = n*n+n+i
			destination = n*(n-1)+i
			if (i%2 == 0):
				origin, destination = destination, origin
			edges.write('	<edge from="{orig}" id="{orig}to{dest}" to="{dest}" numLanes="{lanes}"/>\n'.format(orig=str(origin), dest=str(destination), lanes = str(nlanes)))
			# right
			origin = n*i+n-1
			destination = n*n+2*n+n-i-1
			if (i%2 == 1):
				origin, destination = destination, origin
			edges.write('	<edge from="{orig}" id="{orig}to{dest}" to="{dest}" numLanes="{lanes}"/>\n'.format(orig=str(origin), dest=str(destination), lanes = str(nlanes)))
			# left
			origin = n*n+3*n+i
			destination = n*(n-i-1)
			if (i%2 == 1):
				origin, destination = destination, origin
			edges.write('	<edge from="{orig}" id="{orig}to{dest}" to="{dest}" numLanes="{lanes}"/>\n'.format(orig=str(origin), dest=str(destination), lanes = str(nlanes)))
		edges.write('</edges>\n')

def networkgenerator(l,n, nlanes):
	nodgenerator(l,n) 
	edgegenerator(n, nlanes)
	netconvertProcess = subprocess.call(["netconvert", "-n", "simulations/input/nodes.nod.xml", "-e", "simulations/input/edges.edg.xml", "-o", "simulations/input/mapa.net.xml"])

