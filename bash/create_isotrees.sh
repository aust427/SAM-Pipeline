#!/bin/bash
#SBATCH -J ct_isotree
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --exclusive
#SBATCH --time=100:00:00
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j
#SBATCH -p bnl

module load gcc
module load lib/gsl

CT_DIR=/mnt/ceph/users/agabrielpillai/TNG50/L35n2160TNG_DM/consistent-trees # path to consistent-trees files
SCRIPT_DIR=/mnt/home/agabrielpillai/sc-sam # path to tree_to_isotree.pl script
OUT_DIR=/mnt/ceph/users/agabrielpillai/ # path to output directory
SUBVOLS=6 # how many subvolumes**3 files

source /mnt/home/agabrielpillai/.bashrc
for i in $(seq 0 $(($SUBVOLS - 1)))
do
  for j in $(seq 0 $(($SUBVOLS - 1)))
  do
    for k in $(seq 0 $(($SUBVOLS - 1)))
    do
      perl $SCRIPT_DIR/tree_to_isotree.pl $CT_DIR/"tree_${i}_${j}_${k}.dat" > $OUT_DIR/"isotree_${i}_${j}_${k}.dat"
		done
	done
done
