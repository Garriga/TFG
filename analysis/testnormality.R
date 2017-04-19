#test normality for case0
library(MVN)

setwd('~/TFG')
train <- read.csv('output/train/train.csv', header = TRUE, sep=';')
case0 <- train[train$case == 0,]
data <- case0
data$case <- NULL
uniNorm(data, type = 'SW')
