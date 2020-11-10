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

source /mnt/home/agabrielpillai/.bashrc
for i in {0..5}
do
	for j in {0..5}
	do
		for k in {0..5}
		do
			mkdir /mnt/ceph/users/agabrielpillai/tng-sam/L35n2160TNG/isotrees/"${i}_${j}_${k}" 
			perl /mnt/home/agabrielpillai/sc-sam/tree_to_isotree.pl /mnt/ceph/users/agabrielpillai/TNG50/L35n2160TNG_DM/consistent-trees/"tree_${i}_${j}_${k}.dat" > /mnt/ceph/users/agabrielpillai/tng-sam/L35n2160TNG/isotrees/"${i}_${j}_${k}"/"isotree_${i}_${j}_${k}.dat"
		done
	done
done
