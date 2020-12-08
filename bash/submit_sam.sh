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

SIM=L75n1820TNG # name of simulation and directory 
SUBVOLS=5 # how many subvolumes, such that the total number of isotree files = subvols**3
PARTITION=2 # first index of subvolume, so that you are running subvolume**2 between [PARTITION, 0, 0] and [PARTITION, SUBVOLUME-1, SUBVOLUME-1]

SCRIPT_PATH=/mnt/home/agabrielpillai/scripts/SAM-Pipeline # script location path

IN_PATH=/mnt/ceph/users/agabrielpillai/For_Rachel/IllustrisTNG/$SIM/isotrees # input file directory where the isotrees live
OUT_PATH=/mnt/ceph/users/agabrielpillai/For_Rachel/IllustrisTNG/$SIM/sc-sam # output directory for where sam outputs are going. recommend to not be same as in_path

LIB_PATH=/mnt/home/agabrielpillai/gflib # path to lib information for sam recipes and variance file
SAM_PATH=/mnt/home/agabrielpillai/sc-sam # path to sc-sam location

rm -rf "$OUT_PATH/${PARTITION}"_* # remove everything related to that partition in that output path for clean creation

# generate new directories for each subvolume in the partition 
for j in $(seq 0 $(($SUBVOLS - 1)))
do
  for k in $(seq 0 $(($SUBVOLS - 1)))
  do
    mkdir $OUT_PATH/"${PARTITION}_${j}_${k}"
  done
done

# create new param.scsam and files.list for that partition 
python3 $SCRIPT_PATH/running/gen_files.py $SIM $PARTITION $LIB_PATH $IN_PATH $OUT_PATH

# run the SAM using Python multiprocessing pool
python3 $SCRIPT_PATH/running/run_SAM_multi.py $SIM $PARTITION $OUT_PATH $SAM_PATH $SUBVOLS
