import subprocess

ncases = 8
maxDur = 25
seed_train = 10
seed_test = 20

#put all the generated data for every case in one file (for each case)
#train
subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'train', str(maxDur), str(seed_train), str(ncases)])
#test 
subprocess.call(['Rscript', 'analysis/preprocess/getDataFiles.R', 'test', str(maxDur), str(seed_test), str(ncases)])
