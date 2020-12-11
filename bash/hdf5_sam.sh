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

SIM=L75n1820TNG # what simulation
NSUBVOL=5 # NSUBVOL**3 = how many total subvolumes in this simulation
SNAP_RANGE=0-99 # snapnum range given via galprop + haloprop output file, for ex. '0-99' or '99-99'
SNAPSHOT_OFFSET=0 # value to correct snapshot to max value if consistent-trees skipped early ones
SCRIPT_PATH=/mnt/home/agabrielpillai/scripts/SAM-Pipeline/postprocessing # path to python scripts

IN_PATH=/mnt/ceph/users/agabrielpillai/For_Rachel/IllustrisTNG/$SIM/sc-sam # path to folder containing raw ascii values
OUT_PATH=/mnt/ceph/users/agabrielpillai/For_Shy/tng-sam/$SIM # path to directory to output hdf5 files. DIFFERENT from in_path
REDSHIFT_PATH=/mnt/home/agabrielpillai/scripts/SAM-Pipeline # path to redshift.hdf5 file
# later change this to an if else statement where if directory exists, remove contents, else create
mkdir $OUT_PATH/output

rm -rf $OUT_PATH/output/* # remove subvolume directories and all contents if they exist


for i in $(seq 0 $(($NSUBVOL - 1)))
do
  for j in $(seq 0 $(($NSUBVOL - 1)))
  do
    for k in $(seq 0 $(($NSUBVOL - 1)))
    do
      mkdir $OUT_PATH/output/"${i}_${j}_${k}"  # create subvolume directory
      python3 $SCRIPT_PATH/SAM-hdf5.py $i $j $k $NSUBVOL $IN_PATH $OUT_PATH $SNAP_RANGE $SNAPSHOT_OFFSET $REDSHIFT_PATH
		done
	done
done

mkdir $OUT_PATH/output/lookup
# generate tree offsets for merger tree loading
python3 $SCRIPT_PATH/tree-offsets.py $NSUBVOL $OUT_PATH
