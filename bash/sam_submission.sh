#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J tng-sam-multi-2
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

PARTITION=5
BASE_PATH=/mnt/ceph/users/agabrielpillai/tng-sam
SIM=L35n2160TNG
SUBVOLS=6

python3 /mnt/ceph/users/agabrielpillai/tng-sam/scripts/running/run_SAM_multi.py $PARTITION $SIM $BASE_PATH $SUBVOLS 
