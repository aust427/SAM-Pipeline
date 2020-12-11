import sys
import site

sys.path.append('/mnt/home/agabrielpillai/.local/lib/python3.6/site-packages/')
site.addsitedir('/mnt/home/agabrielpillai/') 
site.addsitedir('/mnt/home/agabrielpillai/scripts/') 

import h5py

import illustris_python as il
import illustris_sam as ilsam

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

basePathSAM = str(sys.argv[1])
matchPath = str(sys.argv[2])
snap_start = int(sys.argv[3])

matches_DM = h5py.File('{}/matches_DM.hdf5'.format(matchPath), 'r')
matches_FP = h5py.File('{}/matches_FP.hdf5'.format(matchPath), 'r')

offset = np.zeros(100)
subvolumes = []

for i in range(5):
    for j in range(5):
        for k in range(5):
            subvolumes.append([i, j, k])

#subvolumes.append([0, 0, 0])

for subvolume in subvolumes: 
    head = ilsam.groupcat.load_header(basePathSAM, subvolume)
    haloprop = ilsam.groupcat.load_haloprop(basePathSAM, subvolume, fields=['HalopropSnapNum'])
    print('haloprop loaded: ', subvolume)

    haloprop_SAM = pd.DataFrame()
    haloprop_SAM['snap_num'] = haloprop['HalopropSnapNum']
    haloprop_SAM['subfind-idx-DM'] = -1
    haloprop_SAM['subfind-idx-FP'] = -1
    haloprop_SAM['fof-idx-DM'] = -1
    haloprop_SAM['fof-idx-FP'] = -1
    
    for i in range(snap_start, 100):
        # get the values in haloprop that are in that snapshot, then pull those out of the match files and assign
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'subfind-idx-DM'] = \
            matches_DM['Subfind'][str(i)][int(offset[i]):int(offset[i]+head['Ngroups_ThisFile_Redshift'][i])][:]
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'fof-idx-DM'] = \
            matches_DM['FoF'][str(i)][int(offset[i]):int(offset[i]+head['Ngroups_ThisFile_Redshift'][i])][:]

        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'subfind-idx-FP'] = \
            matches_FP['Subfind'][str(i)][int(offset[i]):int(offset[i]+head['Ngroups_ThisFile_Redshift'][i])][:]
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'fof-idx-FP'] = \
            matches_FP['FoF'][str(i)][int(offset[i]):int(offset[i]+head['Ngroups_ThisFile_Redshift'][i])][:]
    print('matches appended')

    galprop = ilsam.groupcat.load_galprop(basePathSAM, subvolume, fields=['GalpropHaloIndex', 'GalpropSatType'])
    print('galprop loaded: ', subvolume)

    galprop_SAM = pd.DataFrame()
    galprop_SAM['halo_index'] = galprop['GalpropHaloIndex']
    galprop_SAM['sat_type'] = galprop['GalpropSatType']
    galprop_SAM['subfind-idx-DM'] = -1
    galprop_SAM['subfind-idx-FP'] = -1

    # can just index the values from haloprop rather than doing another loop
    galprop_SAM['subfind-idx-DM'] = haloprop_SAM.iloc[galprop_SAM['halo_index']]['subfind-idx-DM'].values
    galprop_SAM['subfind-idx-FP'] = haloprop_SAM.iloc[galprop_SAM['halo_index']]['subfind-idx-FP'].values

    f = h5py.File('{}/output/{}_{}_{}/matches.hdf5'.format(basePathSAM, *subvolume), 'w')

    subhalos = f.create_group("Galprop")
    subhalos_FP = subhalos.create_dataset('GalpropSubfindIndex_FP', (galprop_SAM.shape[0], ), dtype='int32',
                                          data=galprop_SAM['subfind-idx-FP'])
    subhalos_DM = subhalos.create_dataset('GalpropSubfindIndex_DM', (galprop_SAM.shape[0], ), dtype='int32',
                                          data=galprop_SAM['subfind-idx-DM'])

    halos = f.create_group("Haloprop")
    halos_FP = halos.create_dataset('HalopropFoFIndex_FP', (haloprop_SAM.shape[0], ), dtype='int32',
                                       data=haloprop_SAM['fof-idx-FP'])
    halos_DM = halos.create_dataset('HalopropFoFIndex_DM', (haloprop_SAM.shape[0], ), dtype='int32',
                                          data=haloprop_SAM['fof-idx-DM'])

    f.close()
    print('matches written')
    offset = offset + head['Ngroups_ThisFile_Redshift']
