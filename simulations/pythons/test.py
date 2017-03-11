def simulate(tsim, seed, maxDur, frequency):
    from __future__ import division
    import subprocess, os, csv, time
    start_time = time.time()
    path = os.getcwd() #ends without /

    #RUNNING THE CASES
    cases = ['case0', 'case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7']

    header =  [False]*len(values)

    from pythons import directory
    directory.check('output/')

    directory.check('output/test/')
    directory.check('output/test/detectors/')
    directory.check('output/test/tripinfo/')

    directory.check('output/xml/')

    #run train data
    start_train = time.time()
    #generates de configuration file
    files.configuration(tsim)
    for case in cases:
        start_traffic = time.time()
        print '-------- Generating traffic files --------'
        timesDoc = open("output/train/files/times/travelTime/" + case + ".csv", 'w')
        timesDoc.write('maxDur;meanTime;maxTime\n')
        timesLoss = open("output/train/files/times/timeLoss/" + case + "Loss.csv", 'w')
        timesLoss.write('maxDur;meanLoss;maxLoss\n')
    
        #generates the traffic for the simulation
        tripsGenerator.writeTrips(0, tsim, case, seed)	
        subprocess.call(["duarouter", "-n", "input/mapa.net.xml", "-t", "input/trips.trips.xml", "-o", "input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])    
    
        print 'Traffic generation time: {} seconds'.format(str(time.time() - start_traffic))
        print ''
	##########################
	##########################
	#cal eliminar aquest for
	##########################
	##########################
        for i in range(len(values)):
            maxDur = values[i]
            print '-------- Simulating {case} with  maxDur {maxDur} seconds --------'.format(case = case, maxDur = maxDur)
	    #generate additional file for the simulation
            files.additional(maxDur, frequency)
     
        #runs the simulation
        start_simulation = time.time()
        subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1"])
        print ''
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/train/csv/tripinfo/tripinfo{case}_{maxDur}.csv".format(case = case, maxDur = maxDur))
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/train/csv/detectors/detectors{case}_{maxDur}.csv".format(case = case, maxDur = maxDur))
        print 'Simulation and conversion time {} seconds'.format(str(time.time() - start_simulation))
		
        #write the detectors measures in the csv
        subprocess.call(["Rscript", "postprocess/codes/writeDetectorsCsv.R", str(maxDur), case, str(header[i])])
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

print 'Total time of running train simulations: {} seconds'.format(str(time.time() - start_train))

#cost function

maxDurRef
#running the test data
start_test = time.time()
tsim =5*3600
seed = 20
#generates de configuration file
files.configuration(tsim)
for case in cases:
    start_traffic = time.time()
    print '-------- Generating traffic files --------'
    #generates the traffic for the simulation
    tripsGenerator.writeTrips(0, tsim, case, seed)	
    subprocess.call(["duarouter", "-n", "input/mapa.net.xml", "-t", "input/trips.trips.xml", "-o", "input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])    
    print 'Traffic generation time: {} seconds'.format(str(time.time() - start_traffic))
    print ''

    print '-------- Simulating {case} with  maxDur {maxDur} (reference value) seconds --------'.format(case = case, maxDur = maxDurRef)
    #generate additional file for the simulation
    files.additional(maxDurRef, frequency)
    #runs the simulation
    start_simulation = time.time()
    subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1"])
    print ''
    os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/test/tripinfo/tripinfo{case}_{maxDur}.csv".format(case = case, maxDur = maxDurRef))
    os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/test/detectors/detectors{case}_{maxDur}.csv".format(case = case, maxDur = maxDurRef))
    print 'Simulation and conversion time {} seconds'.format(str(time.time() - start_simulation))	
        
    #write the detectors measures in the csv
    #subprocess.call(["Rscript", "postprocess/codes/writeDetectorsCsv.R", str(maxDurRef), case, str(header[i])])
    #header[i] = True    #once we have written the header it must be true, to avoid writing it again
    #start_writecsv = time.time()        
    
    #print 'Writing travel times: {} seconds'.format(str(time.time() - start_writecsv))         
    #print ''

print 'Total time of running test simulations: {} seconds'.format(str(time.time() - start_test))
print ''
print 'Total time of execution: {} seconds'.format(str(time.time() - start_time))

os.system('rm -r output/xml/')

    Contact GitHub API Training Shop Blog About 

