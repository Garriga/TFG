# TFG
This repository contains in simulations the necessary codes to perform the SUMO simulations with a predefined cases.
It also contains the programs used to analyze the data obtained.

## Simulations
(this doesn't work yet, it is in process)
The reference case is phaseDur of 40 seconds and minDur of 5 seconds.
All the files must be executed having as working directory the simulations folder. 
The file run.py runs the simulations that will be used for training and the simulations that will be used to test the method of classification. Between these two steps, the is a optimization function that decides which is the best maxDur for the reference scenario, which is the one that will be used to run the test data.

## Data analysis


## Requierements
You need to have installed SUMO (Simulation for Urban Mobility), Python and R. 
It is also necessary to have as environment variable the variable SUMO$HOME (that allows SUMO$HOME/tools/...). See more details in the SUMO installation documentation.  
**R packages**: plyr, tictoc

