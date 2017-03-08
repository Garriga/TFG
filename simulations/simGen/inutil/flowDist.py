
def linear(t,tin,tmax,maxflow):
	maxflowposs = 180 # vehicles per minute
	flowparameter = float(maxflow)/maxflowposs
	if (t < tin):
		return 0
	if (t > tmax):
		return float(flowparameter)
	return float((t-tin))/(tmax-tin)*flowparameter
