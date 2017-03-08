library(plyr) #for the function count

#LOAD DATA FILES
#we get a character vector with the routes from the routes file
path <- getwd()
routes <- read.csv(paste(path, "/output/csv/routes.csv", sep=""), sep=";")
#we remove the data that we don't want (it needs to be removed because we are going the use the function
#unique in the dataframe)
routes$vehicle_depart <- NULL
routes$vehicle_id <- NULL

routes$route_edges <- as.character(routes$route_edges)

#we extract the routes names
#routes <- as.character(levels(trips$route_edges))

#FUNCTIONS DEFINITION
extractPath <- function(x) {
  edgeOrigin <- x[1]
  edgeDestination <- x[length(x)]
  return(paste(edgeOrigin, edgeDestination, sep="->"))
}

getPath <- function(row) {
  return(paste(row[1],row[4],sep="->"))
}
  
#PROCESS THE DATA
routes$splittedRoutes <- lapply(routes$route_edges, FUN = function(x) strsplit(x, " ")[[1]])
routes$path <- as.character(lapply(routes$splittedRoutes, extractPath))
routes$path <- as.factor(routes$path) #if we try to convert directly the list to factors is doesn't work
flow <- count(routes, "path")
routes <- unique(routes) #repeted elements are removed
#we give both dataframes the same order
routes <- routes[order(routes$path), ]
flow <- flow[order(flow$path), ]
routes$flow <- flow$freq
routes$route_edges <- NULL

#GENERATE THE F.DAT FILE
writeroute <- function(edges) {
  l <- length(edges)
  cat("[")
  if (l > 1) {
    for (i in 1:(l-1)) {
      cat("'")
      cat(edges[i])
      cat("'")
      cat(", ")
    }
  }
  cat("'")
  cat(edges[l])
  cat("'")
  cat("]")
}
  
printLine <- function(row) {
  idx <- as.character(row$idx)
  cat(paste("\t", idx,":{'path': '", sep = ""))
  cat(as.character(row$path))
  cat("', 'index' : ")
  cat(idx)
  cat(", 'flow' : ")
  cat(as.character(row$flow))
  cat(", 'route' : ")
  writeroute(row$splittedRoutes[[1]])
  cat("},\n")
  return()
}
  
sink(paste(path, "/postprocess/data/F.dat", sep=""))
n <- length(routes$path)
routes$idx <- 0:(n-1)
cat("{\n")

#apply(routes[1:(n-1),], 1, printLine)
if (n > 1) {
  for (i in 1:(n-1)) {
    printLine(routes[i,])
  }
}
#last row (wich is different)
row <- routes[n,]
cat(paste("\t", as.character(row$idx),":{'path': '", sep = ""))
cat(as.character(row$path))
cat("'")
cat(", 'index' : ")
cat(as.character(row$idx))
cat(", 'flow' : ")
cat(as.character(row$flow))
cat(", 'route' : ")
writeroute(row$splittedRoutes[[1]])
cat("}\n")
cat("}")
sink()
