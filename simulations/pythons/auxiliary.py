def check(path):
    import os
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.mkdir(directory)

def getTimes(case, maxDur):
    import csv
    totalTime = 0;
    totalLoss = 0;
    n = 0
    number = {}
    cumTime = {}
    cumLoss = {}
    tripinfo = open ("output/train/csv/tripinfo/tripinfo{case}_{maxDur}.csv".format(case = case, maxDur = maxDur), 'r')
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
