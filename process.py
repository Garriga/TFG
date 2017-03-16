import subprocess

seed_train = 10
seed_test = 20

maxDur = 25
ncases = 8

#put all the generated data for every case in one file (for each case)
#train
subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'train', str(seed_train), str(maxDur), str(ncases)])
#test 
subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'test', str(seed_test), str(maxDur), str(ncases)])
