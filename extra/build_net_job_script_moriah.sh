#!/bin/bash

#SBATCH --time=5-00:00:00
#SBATCH -n5
#SBATCH -c2
#SBATCH --mem-per-cpu=128g
#SBATCH --partition glacier

source /sci/home/nadavkatz/Desktop/MiningBigData/final/bin/activate

python3 -u build_with_breaks.py

deactivate
