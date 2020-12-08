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

SCRIPT_PATH=/mnt/home/agabrielpillai/scripts/SAM-Pipeline/postprocessing # path to python scripts
BASE_PATH=/mnt/ceph/users/agabrielpillai/For_Shy/tng-sam/L75n1820TNG
NSUBVOL=5

# create additional linking parameters between galprop and haloprop for snapshots, useful especially if interested in satellites
python3 $SCRIPT_PATH/append-snap-idx.py $BASE_PATH $NSUBVOL
