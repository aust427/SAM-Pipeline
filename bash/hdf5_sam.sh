#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J hdf5-sam
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

BASE_PATH=/mnt/ceph/users/agabrielpillai/tng-sam
SIM=L35n2160TNG
SUBVOLS=6

for i in {0..5}
do
        for j in {0..5}
        do
                for k in {0..5}
                do
			python3 $BASE_PATH/scripts/postprocessing/SAM-hdf5.py $i $j $k $SUBVOLS $SIM $BASE_PATH
		done
	done
done 
