library(plyr)
library(caTools)
library(tictoc)
tic()
#plot the average travel time 
tripinfo <- read.csv("output/csv/tripinfo/tripinfocase10NE_30.csv", sep = ';')
#tripinfo vehicles are ordered by order of arrival

tripinfo$tripinfo_arrival <- as.numeric(tripinfo$tripinfo_arrival)
tripinfo$tripinfo_duration <- as.numeric(tripinfo$tripinfo_duration)
toc()
getMean <- function(t) {
  meanDur <- mean(tripinfo[tripinfo$tripinfo_arrival == t,]$tripinfo_duration)
  return(meanDur)
}

tsim <-  8*3600;
time <- 1:tsim
duration <- aaply(time, 1, getMean) 
toc()
means <- runmean(duration, 60)
plot(time, duration, pch = '.')
abline(v = 2*3600, col = 'red')
abline(v = 2.5*3600, col = 'red')
abline(v = 5*3600, col = 'blue')
abline(v = 5.5*3600, col = 'blue')

plot(time, means, pch = '.')
abline(v = 2*3600, col = 'red')
abline(v = 2.5*3600, col = 'red')
abline(v = 5*3600, col = 'blue')
abline(v = 5.5*3600, col = 'blue')
