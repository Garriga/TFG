def simulate(tsim, seed, frequency):
    from __future__ import division
    from pythons import directory
    import subprocess, os, time
    start_time = time.time()
    #This reference case considers actuated traffic lights with a phase duration of
    #40 second, a minDur of 5 seconds and a maxDur of 60 seconds.
    path = os.getcwd() #ends without /

    #RUNNING THE CASES
    cases = ['case0', 'case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7']
    values = range(10,61,5)
    header =  [False]*len(values)

    directory.check('output/')
    directory.check('output/test/')
    directory.check('output/test/detectors/')
    directory.check('output/test/tripinfo/')

    directory.check('output/train/')
    directory.check('output/train/files/')
    directory.check('output/train/files/nVeh/')
    directory.check('output/train/files/occupancy/')
    directory.check('output/train/files/speed/')
    directory.check('output/train/files/times/')
    directory.check('output/train/files/times/travelTime/')
    directory.check('output/train/files/times/timeLoss/')
    directory.check('output/train/csv/')
    directory.check('output/train/csv/detectors/')
    directory.check('output/train/csv/tripinfo/')

    directory.check('output/xml/')

    #generates de configuration file
    files.configuration(tsim)
    from pythons import auxiliary as aux
    start_train = time.time()
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
            meanTime, maxTime, meanLoss, maxLoss = aux.getTimes(case, maxDur);
            timesDoc.write(str(maxDur) + ';' + str(meanTime) + ';' + str(maxTime) + '\n')
            timesLoss.write(str(maxDur) + ';' + str(meanLoss) + ';' + str(maxLoss) + '\n')
            print 'Writing travel times: {} seconds'.format(str(time.time() - start_writecsv))         
            print ''
        timesDoc.close()
        timesLoss.close()

    print 'Total time of running train simulations: {} seconds'.format(str(time.time() - start_train))
