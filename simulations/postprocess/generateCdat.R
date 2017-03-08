library(plyr)
path <- getwd()
tll <- read.csv(paste(path, "/netDef/csv/mapa.tll.csv", sep=""), sep=";")
links <- subset(tll, is.na(tll$tlLogic_programID)) 
#edges not controlled by traffic lights sould be discarted in a consecutive subsetting, but we should know 
#how are written the connection if there are not traffic lights (in the grid network every connection has
#a traffic light, so it can't be evaluated)
#we eliminate the NAs
links$tlLogic_programID <- NULL
links$tlLogic_type <- NULL
links$tlLogic_id <- NULL
links$tlLogic_offset <- NULL
links$phase_duration <- NULL
links$phase_state <- NULL
links$tlLogics_version <- NULL
#we eliminate useless data
links$connection_to <- NULL
links$connection_toLane <- NULL
links$connection_fromLane <- NULL

merge <- function(df) {
  df$connection_linkIndex[[1]] <- as.numeric(df$connection_linkIndex)
  return(df[1,])
}

addNum <- function(df) {
  df$num <- length(df$connection_linkIndex)
  return(df)
}

links <- ddply(links, .(connection_tl), addNum)
links$connection_linkIndex <- as.list(links$connection_linkIndex)
links <- ddply(links, .(connection_from), merge)

#THE ORDER IS NOT THE SAME THAN IN E.DAT, BECAUSE HERE NOT EVERY EDGE IS REPRESENTED, ONLY THE EDGES
#CONTROLED BY A TRAFFIC LIGHT

sink(paste(path, "/postprocess/data/C.dat", sep=""))

writelinks <- function(x) {
  l <- length(x)
  cat("[")
  if (l > 1) {
    for (i in 1:(l-1)) {
      cat(x[i])
      cat(", ")
    }
  }
  cat(x[l])
  cat("]")
}

printline <- function(row) {
  cat(paste("\t", row$idx,":{'edge': '", sep = ""))
  cat(as.character(row$connection_from))
  cat("', 'index' : ")
  cat(row$idx)
  cat(", 'numLinks' : ")
  cat(as.character(row$num))
  cat(", 'links' : ")
  writelinks(row$connection_linkIndex[[1]])
  cat("},\n")
  return()
}

n <- length(links$connection_from)
links$idx <- as.character(0:(n-1))
cat("{\n")
#apply(links[1:(n-1),], 1, printline)
for (i in 1:(n-1)) {
  printline(links[i,])
}
row <- links[n,]
cat(paste("\t", row$idx,":{'edge': '", sep = ""))
cat(as.character(row$connection_from))
cat("', 'index' : ")
cat(row$idx)
cat(", 'numLinks' : ")
cat(as.character(row$num))
cat(", 'links' : ")
writelinks(links$connection_linkIndex[[n]])
cat("}\n")
cat("}")
sink()
