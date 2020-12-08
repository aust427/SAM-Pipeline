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
matchPath = '/mnt/home/agabrielpillai/ceph/tng-sam/L75n1820TNG/matches'

matches_DM = h5py.File(matchPath + '/matches_DM.hdf5', 'r')
matches_FP = h5py.File(matchPath + '/matches_FP.hdf5', 'r')

offset = np.zeros(100)
subvolumes = []

for i in range(5):
    for j in range(5):
        for k in range(5):
            subvolumes.append([i, j, k])

# subvolumes.append([0, 0, 0])

for subvolume in subvolumes: 
    head = ilsam.groupcat.load_header(basePathSAM, subvolume)
    haloprop = ilsam.groupcat.load_haloprop(basePathSAM, subvolume, fields=['HalopropSnapNum'])
    print('haloprop loaded: ', subvolume)
    
    haloprop_SAM = pd.DataFrame()
    haloprop_SAM['snap_num'] = haloprop['HalopropSnapNum']
    haloprop_SAM['subfind-idx-DM'] = -1
    haloprop_SAM['subfind-idx-FP'] = -1
    
    for i in range(0, 100):
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'subfind-idx-DM'] = \
            matches_DM[str(i)][int(offset[i]):int(offset[i]+head['Ngroups_ThisFile_Redshift'][i])][:]
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'subfind-idx-FP'] = \
            matches_FP[str(i)][int(offset[i]):int(offset[i]+head['Ngroups_ThisFile_Redshift'][i])][:]
    print('matches appended')
    
    f = h5py.File(basePathSAM + '/output/{}_{}_{}/matches.hdf5'.format(*subvolume), 'r+')
    
    if 'HalopropSubfindID' in f['Haloprop'].keys():
        del f['Haloprop']['HalopropSubfindID']   
        
    if 'HalopropSubfindID_FP' in f['Haloprop'].keys():
        del f['Haloprop']['HalopropSubfindID_FP']    
        
    if 'HalopropSubfindID_DM' in f['Haloprop'].keys():
        del f['Haloprop']['HalopropSubfindID_DM']
    
    subfind_FP = f['Haloprop'].create_dataset('HalopropSubfindID_FP', (haloprop_SAM.shape[0], ), dtype='int32',
                                              data=haloprop_SAM['subfind-idx-FP'].values.astype(float))
    subfind_DM = f['Haloprop'].create_dataset('HalopropSubfindID_DM', (haloprop_SAM.shape[0], ), dtype='int32',
                                              data=haloprop_SAM['subfind-idx-DM'].values.astype(float))
        
    f.close()
    print('matches written')
    offset = offset + head['Ngroups_ThisFile_Redshift']
