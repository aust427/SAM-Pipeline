#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J matches-pre-sam
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

BASE_PATH=/mnt/ceph/users/agabrielpillai/tng-sam

python3 $BASE_PATH/scripts/postprocessing/snap-SAM-match.py

python3 $BASE_PATH/scripts/postprocessing/append-subfind-matches.py 
