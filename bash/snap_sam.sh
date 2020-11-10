#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J append-snap-idx
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

BASE_PATH=/mnt/ceph/users/agabrielpillai/tng-sam

python3 $BASE_PATH/scripts/postprocessing/append-snap-idx.py 
