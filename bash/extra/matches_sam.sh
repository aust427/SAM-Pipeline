#!/bin/bash
#SBATCH --partition=gen
#SBATCH --nodes=1
#SBATCH -J matches-pre-sam
#SBATCH --exclusive
#SBATCH --time=48:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load python3

SIM=L75n1820TNG
# To make life easier, BP = BASE_PATH and not Bolshoi-Planck...
SCRIPT_PATH=/mnt/home/agabrielpillai/scripts/SAM-Pipeline/postprocessing
BP_SAM=/mnt/ceph/users/agabrielpillai/For_Shy/tng-sam/$SIM

BP_TNG_FP=/mnt/ceph/users/sgenel/PUBLIC/IllustrisTNG100/
BP_TNG_DM=/mnt/ceph/users/sgenel/PUBLIC/L75n1820TNG_DM/output

BP_ROCKSTAR=/mnt/ceph/users/agabrielpillai/IllustrisTNG/L75n1820TNG_DM/output

FILE_OUT_PATH=/mnt/ceph/users/agabrielpillai/For_Rachel/IllustrisTNG/$SIM/sc-sam
IMG_OUT_PATH=/mnt/home/agabrielpillai/plots/SAM-matching/L75n1820TNG

SNAP_START=0

# if you want to redo the match file, uncomment the following lines
# rm $FILE_OUT_PATH/matches_DM.hdf5
# rm $FILE_OUT_PATH/matches_FP.hdf5

if [ ! -f $FILE_OUT_PATH/matches_DM.hdf5 ]
then
  echo "Files don't exist, beginning bijective match file creation for DM and FP."
  #python3 $SCRIPT_PATH/snap-SAM-match.py $BP_TNG_FP $BP_SAM $BP_TNG_DM $BP_ROCKSTAR $FILE_OUT_PATH $IMG_OUT_PATH $SNAP_START
fi

python3 $SCRIPT_PATH/append-subfind-matches.py $BP_SAM $FILE_OUT_PATH $SNAP_START
