library(plyr)
library(tictoc)
#preprocesses the data
getDetectors <- function(type, case, maxDur, seed) {
  if (type == 'train') {
    fileName <- paste('output/train/csv/detectors/detectors', case, 'm', maxDur, 's', seed, '.csv', sep = '')
  } else if (type == 'test') {
    fileName <- paste('output/test/detectors/detectors', case, 'm', maxDur, 's', seed, '.csv', sep = '')
  } else if (type == 'NS') {
    fileName <- paste('output/NS/detectors/original/detectors', case, 'm', maxDur, 's', seed, '.csv', sep = '')
  }
  detectors <- read.csv(file = fileName, sep = ";")
  names(detectors) <- substring(names(detectors), 10)
  
  #extracts edge id (we have lane_id)
  extractEdge <- function(s) {
    pos <- regexpr("_", s)
    return(substr(s,1,pos-1))
  }
  detectors$id <- as.character(lapply(detectors$id, extractEdge))
  
  #extract the only relevant variables for us
  detectors <- subset(detectors, select = c(begin, id, nVehContrib))
  
  #we merge data from lanes to get edge data
  merge <- function(df) {
    df$nVehContrib[1] <- sum(df$nVehContrib)
    return(df[1,])
  }
  edges.data <- ddply(detectors, .(begin, id), merge)
  
  #list with the data of every detector
  edges.data <- dlply(edges.data, .(id))
  
  getDf <- function(s) {
    df <- do.call(cbind, lapply(edges.data, function(df) return(df[names(df) == s])))
    names(df) <- names(edges.data)
    return(df)
  }
  var <- 'nVehContrib'
  df <- getDf(var)
  #we remove the first 30 min of simulation because it is not a stationary phase (1 row = 1 min)
  df <- df[31:nrow(df),]
  if (type != 'NS') {
    df$case <- case
  }
  return(df)
}

args <- commandArgs(trailingOnly = TRUE)
type <- args[1]
maxDur <- args[2]
seed <- args[3]
ncases <- as.numeric(args[4])
if (type == 'train') {
  df <- do.call(rbind, llply(0:(ncases-1), function(x) getDetectors(type, x, maxDur, seed)))
  fileOut <- paste('output/', type, '/', type, '.csv', sep = '')
  write.table(df, file = fileOut, sep = ";", quote = FALSE, row.names = FALSE) 
} else if (type == 'test') {
  df <- do.call(rbind, llply(0:(ncases-1), function(x) getDetectors(type, x, maxDur, seed)))
  fileOut <- paste('output/', type, '/', type, '.csv', sep = '')
  write.table(df, file = fileOut, sep = ";", quote = FALSE, row.names = FALSE) 
} else if (type == 'NS') {
  for (i in 1:(ncases-1)) {
    fileOut <- paste('output/NS/detectors/postprocess/case', i, '.csv', sep = '')
    write.table(getDetectors(type, i, maxDur, seed), file = fileOut, sep = ';', quote = FALSE, row.names = FALSE)
    cat('case', i, 'done\n')
  }
}
