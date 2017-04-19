times$cost <- times$meanTime + 2*times$maxTime
mean.min <- min(times$meanTime)
mean.max <- max(times$meanTime)

max.min <- min(times$maxTime)
max.max <- max(times$maxTime)

cost.min <- min(times$cost)
cost.max <- max(times$cost)

mean.range <- 100*(mean.max-mean.min)/mean.max
max.range <- 100*(max.max-max.min)/max.max
cost.range <- 100*(cost.max-cost.min)/cost.max

cat(paste('Mean range: ', mean.range, '\n', sep = ''))
cat(paste('Max range: ', max.range, '\n', sep = ''))
cat(paste('Cost range: ', cost.range, '\n', sep = ''))
