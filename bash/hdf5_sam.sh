#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J hdf5-sam-300
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

BASE_PATH=/mnt/ceph/users/agabrielpillai/tng-sam
SCRIPT_PATH=/mnt/ceph/users/agabrielpillai/tng-sam/scripts/postprocessing
SIM=L205n2500TNG
SUBVOLS=7
SNAP_RANGE=0-98

for i in $(seq 0 $(($SUBVOLS - 1)))
do
        for j in $(seq 0 $(($SUBVOLS - 1)))
        do
                for k in $(seq 0 $(($SUBVOLS - 1)))
                do
			python3 $SCRIPT_PATH/SAM-hdf5.py $i $j $k $SUBVOLS $SIM $BASE_PATH $SNAP_RANGE
		done
	done
done

python3 $SCRIPT_PATH/append-snap-idx.py $SUBVOLS $SIM $BASE_PATH
python3 $SCRIPT_PATH/tree-offsets.py $SUBVOLS $SIM $BASE_PATH 
