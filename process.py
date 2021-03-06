import subprocess
from simulations.pythons import auxiliary as aux
ncases = 8
maxDur = 25
seed_train = 10
#seed_test = 20
#seed_NS = seed_test

#put all the generated data for every case in one file (for each case)
#train
#subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'train', str(maxDur), str(seed_train), str(ncases)])
#subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles3.R', 'train', str(maxDur), str(seed_train), str(ncases)])

#test 
#subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'test', str(maxDur), str(seed_test), str(ncases)])
#subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles3.R', 'test', str(maxDur), str(seed_train), str(ncases)])

#non stationary
for seed in range(20, 111, 10):
	subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'NS', str(maxDur), str(seed), str(ncases)])
	#subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles3.R', 'NS', str(maxDur), str(seed_test), str(ncases)])

#predicts the time for several cases
aux.check('analysis/models/')
