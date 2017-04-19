algorithms <- c('bayes', 'kernel', 'neural_network', 'decision_tree', 'nearest_neighbour')
for (algorithm in algorithms) {
print(algorithm)
filename <- paste('output/NS/detection/detectionTimes_', algorithm, '.csv', sep = '')
data <- read.csv(filename, sep = ';')
#we check if there are errors
data$correct <- (data$t_detection.min.) > 0 & (data$case == data$label)


getMeanDetectionTime <- function(df) {
 df <- df[df$correct,]  #we only consider the correct ones
 return(mean(df$t_detection.min.))
}
getError <- function(df) {
  corrects <- sum(df$correct)
  total <- length(df$correct)
  return(1-corrects/total)
}

library(plyr)
split <- dlply(data, .(consecutive), NULL)
error <- laply(split, getError)
meanDetectionTime <- laply(split, getMeanDetectionTime)

df <- cbind(1:5, error, meanDetectionTime)
colnames(df) <- c('consecutive', 'error', 'mean_detection')

fileout <- paste('output/NS/detection/summary_', algorithm, '.csv', sep = '')
write.table(df, file = fileout, col.names = TRUE, row.names = FALSE, sep = ';')
}