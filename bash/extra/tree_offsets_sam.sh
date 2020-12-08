#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J tree_offsets
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

SIM=L75n1820TNG
NSUB=1
SCRIPT_PATH=/mnt/home/agabrielpillai/scripts/SAM-Pipeline/postprocessing # path to python scripts
BASE_PATH=/mnt/ceph/users/agabrielpillai/For_Shy/tng-sam/$SIM

python3 $SCRIPT_PATH/tree-offsets.py $NSUB $BASE_PATH
