#!/usr/bin/env python
from __future__ import division
import subprocess, imp, os, csv, time
start_time = time.time()
################################################################################
#								PROGRAM INFO							       #
################################################################################
#this algorithm runs every case in a defined basic scenario (reference case).
#This reference case considers actuated traffic lights with a phase duration of 
#40 second, a minDur of 5 seconds and a maxDur of 60 seconds. 

#The cases are defined as new flows (that may be equal to some of the reference flows).

#we build a matrix that contains the mean of the detectors lectures by street.

#a table of mean travel time and max mean travel time per route is also generated at every 
#anomaly case in order to obtain an optimal minDur for the actuated program of the traffic lights. 

#simulation global parameters
tsim = 8*3600
n = 5
l = 150
frequency = 60
seed = 20   #change the seed, the reference was 10
################################################################################
#                       AUXILIARY FUNCTIONS                                    #
################################################################################
def getTimes(case, maxDur):
    totalTime = 0;
    totalLoss = 0;
    n = 0
    number = {}
    cumTime = {}
    cumLoss = {}
    tripinfo = open ("output/csv/tripinfo/tripinfo{case}_{maxDur}.csv".format(case = case, maxDur = maxDur), 'r')
    reader = csv.reader(tripinfo, delimiter = ';')
    row = next(reader)
    posTime = row.index('tripinfo_duration')
    posOrig = row.index('tripinfo_departLane')
    posDest = row.index('tripinfo_arrivalLane')
    posLoss = row.index('tripinfo_timeLoss')    
    for row in reader:
        totalTime += float(row[posTime])
        totalLoss += float(row[posLoss])
        n += 1
        trip = getTrip(row[posOrig], row[posDest])
        if trip in number.keys():
            number[trip] += 1
            cumTime[trip] += float(row[posTime])
            cumLoss[trip] += float(row[posLoss])
        else:
            number[trip] = 1
            cumTime[trip] = float(row[posTime])
            cumLoss[trip] = float(row[posLoss])
    meanTime = totalTime/n
    meanLoss = totalLoss/n
    means = []
    meansLoss = []
    for k in number.keys():
        means.append(cumTime[k]/number[k])
        meansLoss.append(cumLoss[k]/number[k])
    maxTime = max(means)
    maxLoss = max(meansLoss)
    return meanTime, maxTime, meanLoss, maxLoss
            

def getTrip(departLane, arrivalLane):
    departEdge = departLane[0:(departLane.index('_')-1)]
    arrivalEdge = arrivalLane[0:(arrivalLane.index('_')-1)]
    return departEdge + '->' + arrivalEdge

################################################################################
#								NETWORK GENERTION						       #
################################################################################
path = os.getcwd() #ends without /

modl = imp.load_source('networkgenerator', path + '/simGen/networkgenerator.py')
import networkgenerator
modl = imp.load_source('files', path + '/pythons/files.py')	
import files	
modl = imp.load_source('tripsGenerator', path + '/simGen/tripsGenerator.py')
import tripsGenerator

#generates the network
networkgenerator.networkgenerator(l,n)

#generates the necessary files (C.dat, J.dat, E.dat ...)
files.dat()

#generates de configuration file
files.configuration(tsim);

################################################################################
#								RUNNING THE CASES							   #
################################################################################
#cases = ['case0', 'case1', 'case2', 'case3']    #names of the flow files must be: case0.dat, case1.dat, case2.dat, etc
cases = ['case1NE', 'case2NE', 'case3NE', 'case4NE', 'case5NE', 'case6NE', 'case7NE', 'case8NE', 'case9NE', 'case10NE', 'case11NE', 'case12NE', 'case13NE']

#values = range(30,61,5)
values = [30];    #only for the reference case

header =  [False]*len(values)

for case in cases:
    start_traffic = time.time()
    print '-------- Generating traffic files --------'
    timesDoc = open("output/files/times/travelTime/" + case + ".csv", 'w')
    timesDoc.write('maxDur;meanTime;maxTime\n')
    timesLoss = open("output/files/times/timeLoss/" + case + "Loss.csv", 'w')
    timesLoss.write('maxDur;meanLoss;maxLoss\n')
    
    #generates the traffic for the simulation
    tripsGenerator.writeTrips(0, tsim, case, seed)	
    subprocess.call(["duarouter", "-n", "input/mapa.net.xml", "-t", "input/trips.trips.xml", "-o", "input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])    
    
    print 'Traffic generation time: {} seconds'.format(str(time.time() - start_traffic))
    print ''

    for i in range(len(values)):
        maxDur = values[i]
        print '-------- Simulating {case} with  maxDur {maxDur} seconds --------'.format(case = case, maxDur = maxDur)
		#generate additional file for the simulation
        files.additional(maxDur, frequency)
     
        #runs the simulation
        start_simulation = time.time()
        subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1"])
        print ''
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/csv/tripinfo/tripinfo{case}_{maxDur}.csv".format(case = case, maxDur = maxDur))
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/csv/detectors/detectors{case}_{maxDur}.csv".format(case = case, maxDur = maxDur))
        print 'Simulation and conversion time {} seconds'.format(str(time.time() - start_simulation))
		
        #write the detectors measures in the csv
        subprocess.call(["Rscript", "analisi_resultats/writeDetectorsCsv.R", str(maxDur), case, str(header[i])])
        header[i] = True    #once we have written the header it must be true, to avoid writing it again
        start_writecsv = time.time()        
        #travel times depending on tls configuration
        meanTime, maxTime, meanLoss, maxLoss = getTimes(case, maxDur);
        timesDoc.write(str(maxDur) + ';' + str(meanTime) + ';' + str(maxTime) + '\n')
        timesLoss.write(str(maxDur) + ';' + str(meanLoss) + ';' + str(maxLoss) + '\n')
        print 'Writing travel times: {} seconds'.format(str(time.time() - start_writecsv))         
        print ''
    timesDoc.close()
    timesLoss.close()

print 'Total time of execution: {} seconds'.format(str(time.time() - start_time))

