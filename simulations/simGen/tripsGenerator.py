from __future__ import division
import datetime, numpy, math

def writeTrips(tbegin, tend, fileName, seed): 
	numpy.random.seed(seed)

	class flow(object):
		def __init__(self, ID):
			self.ID = ID
		def setValues(self, org, dest, flow0, maxflow, t0, tf, shape, n):		
			self.org = org
			self.dest = dest
			self.flow0 = flow0
			self.maxFlow = maxflow	#cars/min
			self.t0 = t0
			self.tf = tf
			self.shape = shape
			self.n = n
		#shape: L->linear, 'Q'-> quadratic
	
	#LOAD FLOWS DEFINITION DATA
	F = eval(open("simulations/simGen/cases/" + fileName + ".dat").read())
	flows = []
	for f in F:
		FLOW = flow(F[f]['index'])	
		FLOW.setValues(F[f]['origin'], F[f]['destination'], F[f]['flow0'], F[f]['maxFlow'], F[f]['t0'], F[f]['tf'], F[f]['shape'], F[f]['n'])
		flows.append(FLOW)
	
	def growth(y0, x0, y, x, xbegin, xend, shape):
		exp = []
		exp0 = y0
		expmax = y
		if (shape == 'L'):
			m = (y-y0)/(x-x0)
			for i in range(tbegin, tend):
				if (i < x0): exp.append(exp0)
				elif (i > x): exp.append(expmax)
				else: exp.append(exp0+m*(i-x0))
		elif (shape == 'Q'):
			a = (y-y0)/(x-x0)**2
			for i in range(tbegin, tend):
				if (i < x0): exp.append(exp0)
				elif (i > x): exp.append(expmax)
				else: exp.append(a*(i-x0)**2+y0)
		return(exp)


	def writeLines(flow, idx, tbegin, tend):
		trip = '\t<trip id="{id}" depart="{dep}" from="{org}" to="{to}" />\n'	
		#the number of vehicles inseted every second follows a binomial distribution
		n = flow.n
		exp = growth(flow.flow0/60, flow.t0, flow.maxFlow/60, flow.tf, tbegin, tend, flow.shape)	
		for t in range(tbegin, tend):
			p = exp[t]/n
			if(p > 1):
				print("Error, p > 1, the value is: {}".format(str(p)))
			x = numpy.random.binomial(n,p)
			for i in range(x):
				trips.write(trip.format(id = str(idx), dep = str(t), org = flow.org, to = flow.dest))
				idx += 1
		return(idx)
	
	with open("simulations/input/trips.trips.xml", 'w') as trips: 
		trips.write("<!-- generated on {} by tripsGenerator.py-->\n".format(datetime.datetime))
		trips.write("<trips>\n")
		
		idx = 0
		for flow in flows:
			idx = writeLines(flow, idx, tbegin, tend)

		trips.write("</trips>")
