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

basePathSAM = '/mnt/ceph/users/agabrielpillai/tng-sam/L75n1820TNG/'

offset = np.zeros(100)
subvolumes = []

for i in range(5):
    for j in range(5):
        for k in range(5):
            subvolumes.append([i, j, k])

# subvolumes.append([0, 0, 0])
# subvolumes.append([0, 0, 1])

for subvolume in subvolumes: 
    head = ilsam.groupcat.load_header(basePathSAM, subvolume)
    haloprop = ilsam.groupcat.load_haloprop(basePathSAM, subvolume, fields=['HalopropSnapNum', 'HalopropIndex'])
    print('haloprop loaded:', subvolume)

    haloprop_SAM = pd.DataFrame()
    haloprop_SAM['snap_num'] = haloprop['HalopropSnapNum']
    haloprop_SAM['idx'] = haloprop['HalopropIndex']
    haloprop_SAM['snap-idx'] = -1

    for i in range(0, 100):
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'snap-idx'] = np.arange(0, head['Ngroups_ThisFile_Redshift'][i]) + offset[i]

    galprop = ilsam.groupcat.load_galprop(basePathSAM, subvolume, fields=['GalpropHaloIndex', 'GalpropRedshift'])
    print('galprop loaded:', subvolume)
    galprop_SAM = pd.DataFrame()
    galprop_SAM['HaloIndex'] = galprop['GalpropHaloIndex']
    galprop_SAM['redshift'] = galprop['GalpropRedshift']
    galprop_SAM['halo-snap-idx'] = haloprop_SAM.loc[galprop_SAM['HaloIndex'] - 1, 'snap-idx'].values
    print('snap appended')
    
    f = h5py.File(basePathSAM  + '/outputs/subvolume_%i_%i_%i.hdf5' % (subvolume[0], subvolume[1], subvolume[2]), 'r+')
    
    if 'HalopropIndex_Snapshot' in f['Haloprop'].keys():
        del f['Haloprop']['HalopropIndex_Snapshot']          
    if 'GalpropHaloIndex_Snapshot' in f['Galprop'].keys():
        del f['Galprop']['GalpropHaloIndex_Snapshot']     
        
    if 'HalopropIndex_Snapshot' in f['Galprop'].keys():
        del f['Galprop']['HalopropIndex_Snapshot']    
    if 'GalpropHaloIndex_Snapshot' in f['Haloprop'].keys():
        del f['Haloprop']['GalpropHaloIndex_Snapshot']     
    
    idx_haloprop = f['Haloprop'].create_dataset('HalopropIndex_Snapshot', (haloprop_SAM.shape[0], ), 
                                           dtype='int32', data = haloprop_SAM['snap-idx'].values.astype(float)) 
    
    idx_galprop = f['Galprop'].create_dataset('GalpropHaloIndex_Snapshot', (galprop_SAM.shape[0], ), 
                                           dtype='int32', data = galprop_SAM['halo-snap-idx'].values.astype(float))
        
    f.close()
    print('matches written')
    offset = offset + head['Ngroups_ThisFile_Redshift']
