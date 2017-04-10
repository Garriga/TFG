import subprocess, time, os
from simulations.pythons import files
from simulations.simGen import tripsGenerator
from simulations.pythons import auxiliary as aux

#generates the data used for train 
def train(tsim, seed, values, frequency, ncases):
    start_time = time.time()

    cases = range(0,ncases)

    aux.check('output/train/')
    aux.check('output/train/times/')
    aux.check('output/train/times/travelTime/')
    aux.check('output/train/times/timeLoss/')
    aux.check('output/train/csv/')
    aux.check('output/train/csv/detectors/')
    aux.check('output/train/csv/tripinfo/')

    aux.check('output/xml/')

    #generates de configuration file
    files.configuration(tsim)
    start_train = time.time()
    for case in cases:
        start_traffic = time.time()
        print '-------- Generating traffic files --------'
        timesDoc = open("output/train/times/travelTime/" + 'case' + str(case) + ".csv", 'w')
        timesDoc.write('maxDur;meanTime;maxTime\n')
        timesLoss = open("output/train/times/timeLoss/" + 'case' + str(case) + "Loss.csv", 'w')
        timesLoss.write('maxDur;meanLoss;maxLoss\n')
    
        #generates the traffic for the simulation
        tripsGenerator.writeTrips(0, tsim, 'case' + str(case), seed)	
        subprocess.call(["duarouter", "-n", "simulations/input/mapa.net.xml", "-t", "simulations/input/trips.trips.xml", "-o", "simulations/input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])    
    
        print 'Traffic generation time: {} seconds'.format(str(time.time() - start_traffic))
        print ''

        for i in range(len(values)):
            maxDur = values[i]
            print '-------- Simulating case {case} with  maxDur {maxDur} seconds --------'.format(case = case, maxDur = maxDur)
	        #generate additional file for the simulation
            files.additional(maxDur, frequency)
     
            #runs the simulation
            start_simulation = time.time()
            subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1", "--seed", str(seed)])
            print ''
            os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/train/csv/tripinfo/tripinfo{case}m{maxDur}s{seed}.csv".format(case = case, maxDur = maxDur, seed = seed))
            os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/train/csv/detectors/detectors{case}m{maxDur}s{seed}.csv".format(case = case, maxDur = maxDur, seed = seed))
            print 'Simulation and conversion time {} seconds'.format(str(time.time() - start_simulation))
		
            #travel times depending on tls configuration
            start_gettimes = time.time()
            meanTime, maxTime, meanLoss, maxLoss = aux.getTimes(case, maxDur, seed);
            timesDoc.write(str(maxDur) + ';' + str(meanTime) + ';' + str(maxTime) + '\n')
            timesLoss.write(str(maxDur) + ';' + str(meanLoss) + ';' + str(maxLoss) + '\n')
            print 'Get travel times: {} seconds'.format(str(time.time() - start_gettimes))         
            print ''
        timesDoc.close()
        timesLoss.close()

    print '\nTotal time of running train simulations: {} seconds'.format(str(time.time() - start_time))
    print '_______________________________________________________________\n'

#generates the data used for test
def test(tsim, seed, maxDur, frequency,ncases):
    #it differs from the train function because in this case there is only one maxDur 
    #and then the files containing the times are not required
    start_time = time.time()

    cases = range(0,ncases)
    
    aux.check('output/')

    aux.check('output/test/')
    aux.check('output/test/detectors/')
    aux.check('output/test/tripinfo/')

    aux.check('output/xml/')

    #generates de configuration file
    files.configuration(tsim)
    
    for case in cases:
        start_traffic = time.time()
        print '-------- Generating traffic files --------'
        #generates the traffic for the simulation
        tripsGenerator.writeTrips(0, tsim, 'case' + str(case), seed)	
        subprocess.call(["duarouter", "-n", "simulations/input/mapa.net.xml", "-t", "simulations/input/trips.trips.xml", "-o", "simulations/input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])    
    
        print 'Traffic generation time: {} seconds'.format(str(time.time() - start_traffic))
        print ''
	    
        print '-------- Simulating case {case} with  maxDur of reference {maxDur} seconds --------'.format(case = case, maxDur = maxDur)
	    #generate additional file for the simulation
        files.additional(maxDur, frequency)
     
        start_simulation = time.time()        
        #runs the simulation
        subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1", "--seed", str(seed)])
        print ''
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/test/tripinfo/tripinfo{case}m{maxDur}s{seed}.csv".format(case = case, maxDur = maxDur, seed = seed))
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/test/detectors/detectors{case}m{maxDur}s{seed}.csv".format(case = case, maxDur = maxDur, seed = seed))
        print 'Simulation and conversion time {} seconds'.format(str(time.time() - start_simulation))
        
    print '\nTotal time of running test simulations: {} seconds'.format(str(time.time() - start_time))
    print '_______________________________________________________________\n'

def nonstationary(tsim, seed, maxDur, frequency,ncases):
    #it differs from the train function because in this case there is only one maxDur 
    #and then the files containing the times are not required
    start_time = time.time()

    cases = range(1,ncases) #no case0NE
    
    aux.check('output/')

    aux.check('output/NS/')
    aux.check('output/NS/detectors/')
    aux.check('output/NS/tripinfo/')

    aux.check('output/xml/')

    #generates de configuration file
    files.configuration(tsim)
    
    for case in cases:
        start_traffic = time.time()
        print '-------- Generating traffic files --------'
        #generates the traffic for the simulation
        tripsGenerator.writeTrips(0, tsim, 'case' + str(case) + 'NS', seed)	
        subprocess.call(["duarouter", "-n", "simulations/input/mapa.net.xml", "-t", "simulations/input/trips.trips.xml", "-o", "simulations/input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])    
    
        print 'Traffic generation time: {} seconds'.format(str(time.time() - start_traffic))
        print ''
	    
        print '-------- Simulating case NS {case} with  maxDur of reference {maxDur} seconds --------'.format(case = case, maxDur = maxDur)
	    #generate additional file for the simulation
        files.additional(maxDur, frequency)
     
        start_simulation = time.time()        
        #runs the simulation
        subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1", "--seed", str(seed)])
        print ''
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/NS/tripinfo/tripinfo{case}m{maxDur}s{seed}.csv".format(case = case, maxDur = maxDur, seed = seed))
        os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/NS/detectors/detectors{case}m{maxDur}s{seed}.csv".format(case = case, maxDur = maxDur, seed = seed))
        print 'Simulation and conversion time {} seconds'.format(str(time.time() - start_simulation))
        
    print '\nTotal time of running non-stationary simulations: {} seconds'.format(str(time.time() - start_time))
    print '_______________________________________________________________\n'
    
def changeTLS(t_change, t_sim, seed, maxDur1, maxDur2, frequency, case, algorithm):
	
    aux.check('output/')
    aux.check('output/changeTLS/')
    aux.check('output/changeTLS/detectors/')
    aux.check('output/changeTLS/detectors/' + algorithm + '/')
    aux.check('output/changeTLS/tripinfo/')
    aux.check('output/changeTLS/tripinfo/' + algorithm + '/')
    
    aux.check('output/xml/')
    
    #generates the traffic for the simulation
    tripsGenerator.writeTrips(0, t_sim, 'case' + str(case), seed)	
    subprocess.call(["duarouter", "-n", "simulations/input/mapa.net.xml", "-t", "simulations/input/trips.trips.xml", "-o", "simulations/input/rutes.rou.xml", "--unsorted-input", "true", "--ignore-errors", "true", "--departspeed", "10", "--departlane", "free"])
    
    #runs the simulation
    files.additional(maxDur1, frequency)
    files.configuration2(0,t_change)
    subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1", "--seed", str(seed), "--save-state.times", str(t_change), "--save-state.files", "state.sbx"])
    os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/tripinfo1.csv")
    os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/detectors1.csv")
    #reconfigure the tls
    files.configuration2(t_change, t_sim)
    files.additional(maxDur2, frequency)
    #continue the simulation with the new configuration
    subprocess.call(["sumo", "-c", "configuration.sumocfg", "--xml-validation", "never", "--time-to-teleport", "-1", "--seed", str(seed), "--load-state", "state.sbx"])
    
    os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/tripinfo.xml -o output/tripinfo2.csv")
    os.system("$SUMO_HOME/tools/xml/xml2csv.py output/xml/detectors.xml -o output/detectors2.csv")
	
	#merge the files into one
    os.system("mv output/tripinfo1.csv output/changeTLS/tripinfo/{algorithm}/tripinfo{case}s{seed}.csv".format(
		algorithm = algorithm, case = case, seed = seed))
    os.system("tail -n +2 output/tripinfo2.csv >> output/changeTLS/tripinfo/{algorithm}/tripinfo{case}s{seed}.csv".format(
		algorithm = algorithm, case = case, seed = seed))
    
    os.system("mv output/detectors1.csv output/changeTLS/detectors/{algorithm}/detectors{case}s{seed}.csv".format(
		algorithm = algorithm, case = case, seed = seed))
    os.system("tail -n +2 output/detectors2.csv >> output/changeTLS/detectors/{algorithm}/detectors{case}s{seed}.csv".format(
		algorithm = algorithm, case = case, seed = seed))
    
    os.system("rm output/detectors2.csv")
    os.system("rm output/tripinfo2.csv")
