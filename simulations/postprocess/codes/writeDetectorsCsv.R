library(tictoc, quietly = TRUE)
library(plyr, quietly = TRUE)
tic()
args <- commandArgs(trailingOnly = TRUE)
maxDur <- args[1]
case <- args[2]
header <- args[3]
#extract inductionLoops data
detName <- paste("output/csv/detectors/detectors", case, '_', maxDur, '.csv', sep = '')
detectors <- read.csv(detName, sep = ";")
#we preprocess the data.frame changing to most apropriate names
names(detectors) <- substring(names(detectors), 10)
#extract the edge names
extractEdge <- function(s) {
  pos <- regexpr("_", s)
  return(substr(s,1,pos-1))
}
detectors$id <- as.character(lapply(detectors$id, extractEdge))

getMeanEdge <- function(df) {
  df$flow[1] <- 3*mean(df$flow)
  df$length[1] <- mean(df$length[df$length != -1])
  df$nVehContrib[1] <- 3*mean(df$nVehContrib)
  df$nVehEntered[1] <- 3*mean(df$nVehEntered)
  df$occupancy[1] <- mean(df$occupancy)  
  df$speed[1] <- mean(df$speed[df$speed != -1])
  return(df[1,])
}

edges.data <- dlply(detectors, .(id), getMeanEdge)

var <- list("flow", "length", "nVehContrib", "nVehEntered", "occupancy", "speed")

getDf <- function(s) {
  extract <- function(df) {
    names(df)[names(df) == s] <- 
      return(df[names(df) == s])
  }
  df <- do.call(cbind, lapply(edges.data, extract))
  names(df) <- names(edges.data)
  return(df)
}

measures <- lapply(var, getDf)
names(measures) <- var
speedFile <- sprintf("output/files/speed/speed%s.csv", maxDur)
nVehFile <- sprintf("output/files/nVeh/nVeh%s.csv", maxDur)
occupancyFile <- sprintf("output/files/occupancy/occupancy%s.csv", maxDur)
if (header == 'False') {
  #write.table(c('case', names(measures[['nVehContrib']])), file = nVehFile, quote = FALSE, sep = ';', col.names = FALSE, row.names = FALSE)
  #write.table(c('case', names(measures[['speed']])), file = speedFile, quote = FALSE, sep = ';', col.names = FALSE, row.names = FALSE)
  #write.table(c('case', names(measures[['occupancy']])), file = occupancyFile, quote = FALSE, sep = ';', col.names = FALSE, row.names = FALSE)
  write.table(c(case, measures[['nVehContrib']]), file = nVehFile, quote = FALSE, sep = ';', col.names = c('case', names(measures[['nVehContrib']])), row.names = FALSE)
  write.table(c(case, measures[['speed']]), file = speedFile, quote = FALSE, sep = ';', col.names = c('case', names(measures[['speed']])), row.names = FALSE)
  write.table(c(case, measures[['occupancy']]), file = occupancyFile, quote = FALSE, sep = ';', col.names = c('case', names(measures[['speed']])), row.names = FALSE)
  
} else {
write.table(c(case, measures[['nVehContrib']]), file = nVehFile, quote = FALSE, append=TRUE, sep = ';', col.names = FALSE, row.names = FALSE)
write.table(c(case, measures[['speed']]), file = speedFile, quote = FALSE, append=TRUE, sep = ';', col.names = FALSE, row.names = FALSE)
write.table(c(case, measures[['occupancy']]), file = occupancyFile, quote = FALSE, append=TRUE, sep = ';', col.names = FALSE, row.names = FALSE)
}
cat('Detectors data process time: ')
toc()
