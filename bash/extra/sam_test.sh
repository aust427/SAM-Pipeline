#!/bin/bash
#SBATCH -J 0_0_0
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --exclusive
#SBATCH --time=100:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j
#SBATCH -p cca

module load gcc 

/mnt/home/agabrielpillai/sc-sam/gf /mnt/ceph/users/agabrielpillai/For_Rachel/IllustrisTNG/L75n1820TNG/sc-sam/0_0_0/param.scsam > /mnt/ceph/users/agabrielpillai/For_Rachel/IllustrisTNG/L75n1820TNG/sc-sam/0_0_0/progress.log
