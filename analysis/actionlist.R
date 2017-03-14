#cost function
cost <- function(row, opt) {
  if (row[2] > 1.05*opt) return(1e5) #row[2] = meanTime
  return(row[2] + 2*row[3])  #row[3] = maxTime
}

args <- commandArgs(trailingOnly = TRUE)
#n <- as.numeric(args[1])
cases <- paste('case', 0:(n-1), sep = '')

maxDur <- integer(n)
for (k in 1:n) {
  case <- cases[k]
  #loading data
  tableName <- paste("output/train/times/travelTime/", case, ".csv", sep = '')
  times <- read.csv (tableName, sep = ';')
  #computing costs
  costs <- apply(times, 1, function(row) cost(row, min(times$mean)))
  #saving optimal value
  minCost <- which.min(costs)
  maxDur[k] <- times$maxDur[minCost]
}
write.table(cbind(cases, maxDur), file = "output/actionList.txt", row.names = FALSE, quote = FALSE)
cat(maxDur[1])