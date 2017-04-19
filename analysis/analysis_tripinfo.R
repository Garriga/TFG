getMean <- function(df) {
  return(mean(df$duration))
}
compute_cost <- function(mean, maximum, opt) {
  if (!is.null(opt)) {
    if (mean > 1.05*opt) {return(1e5)}
  }
  return(mean + 2*maximum)
}
#load data
maxDur <- 25
seed <- 20
algorithms = c('bayes', 'decision_tree', 'kernel', 'nearest_neighbour', 'neural_network')
for (algorithm in algorithms) {
  costs <- NULL
  for (case in 1:7) {
    #filename = paste('output/NS/tripinfo/tripinfo', case, 'm', maxDur, 's', seed, '.csv', sep = '')
    filename = paste('output/changeTLS/tripinfo/', algorithm, '/tripinfo', case, 's', seed, '.csv', sep = '')
    timesname = paste('output/train/times/travelTime/case', case, '.csv', sep = '')

    data <- read.csv(filename, sep = ';')
    names(data) <- substring(names(data), 10)
    #we remove data from the first 30 min
    data <- data[data$depart >= 30*60,]
    times <- read.csv(timesname, sep = ';')

    #get each vehicle trip
    data$departEdge <- substr(data$departLane, 1, regexpr('_', data$departLane) - 1)
    data$arrivalEdge <- substr(data$arrivalLane, 1, regexpr('_', data$arrivalLane) - 1)
    data$trip <- paste(data$departEdge, data$arrivalEdge, sep = '->')

    #split data by trip
    library(plyr)
    trips.data <- dlply(data, .(trip), NULL)

    means <- laply(trips.data, getMean)

    #compute the cost function
    global_cost <- compute_cost(mean(data$duration), max(means), NULL)

    data1 <- data[data$arrival <= 90*60,]
    trips1.data <- dlply(data1, .(trip), NULL)
    means1 <- laply(trips1.data, getMean)
    cost1 <- compute_cost(mean(data1$duration), max(means1), 109.431984276)

    data2 <- data[data$depart >= 120*60,]
    trips2.data <- dlply(data2, .(trip), NULL)
    means2 <- laply(trips2.data, getMean)
    cost2 <- compute_cost(mean(data2$duration), max(means2), min(times$meanTime))

    costs <- rbind(costs, c(case, cost1, cost2, global_cost))
  }
  output = paste('output/changeTLS/costs/', algorithm, '.csv', sep = '')
  #output = 'output/NS/costsNS.csv'
  write.table(costs, file = output, row.names = FALSE, 
            col.names = c('case', 'cost1', 'cost2', 'global_cost'), sep = ';')
}
#plot one route
#df <- trips.data[[1]]
#plot(df$duration)
