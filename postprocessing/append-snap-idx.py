import sys
import site
import pandas as pd
import numpy as np
import h5py

site.addsitedir('/mnt/home/agabrielpillai/scripts/')
import illustris_sam as ilsam

basePathSAM = str(sys.argv[1])
nsubvol = int(sys.argv[2])

offset = np.zeros(100)
subvolumes = []

for i in range(nsubvol):
    for j in range(nsubvol):
        for k in range(nsubvol):
            subvolumes.append([i, j, k])


for subvolume in subvolumes: 
    head = ilsam.groupcat.load_header(basePathSAM, subvolume)
    haloprop = ilsam.groupcat.load_haloprop(basePathSAM, subvolume, fields=['HalopropSnapNum', 'HalopropIndex'])
    print('haloprop loaded:', subvolume)

    haloprop_SAM = pd.DataFrame()
    haloprop_SAM['snap_num'] = haloprop['HalopropSnapNum']
    haloprop_SAM['idx'] = haloprop['HalopropIndex']
    haloprop_SAM['snap-idx'] = -1

    # find the indices in that snapshot, assign (0, 1, ..., n_items) + offset to those indices
    for i in range(0, 100):
        haloprop_SAM.loc[haloprop_SAM['snap_num'] == i, 'snap-idx'] = \
            np.arange(0, head['Ngroups_ThisFile_Redshift'][i]) + offset[i]

    galprop = ilsam.groupcat.load_galprop(basePathSAM, subvolume, fields=['GalpropHaloIndex', 'GalpropRedshift'])
    print('galprop loaded:', subvolume)
    galprop_SAM = pd.DataFrame()
    galprop_SAM['HaloIndex'] = galprop['GalpropHaloIndex']
    galprop_SAM['redshift'] = galprop['GalpropRedshift']
    # can use halo_index to just pull the value from haloprop, don't have to do any looping here
    galprop_SAM['halo-snap-idx'] = haloprop_SAM.loc[galprop_SAM['HaloIndex'], 'snap-idx'].values
    print('snap appended')

    f = h5py.File('{}/output/{}_{}_{}/subvolume.hdf5'.format(basePathSAM,  *subvolume), 'r+')

    # remove these keys if they already exist in the file
    if 'HalopropIndex_Snapshot' in f['Haloprop'].keys():
        del f['Haloprop']['HalopropIndex_Snapshot']          
    if 'GalpropHaloIndex_Snapshot' in f['Galprop'].keys():
        del f['Galprop']['GalpropHaloIndex_Snapshot']     

    # add these new keys to the files
    idx_haloprop = f['Haloprop'].create_dataset('HalopropIndex_Snapshot', (haloprop_SAM.shape[0], ), dtype='int32',
                                                data=haloprop_SAM['snap-idx'].values.astype(float))
    
    idx_galprop = f['Galprop'].create_dataset('GalpropHaloIndex_Snapshot', (galprop_SAM.shape[0], ), dtype='int32',
                                              data=galprop_SAM['halo-snap-idx'].values.astype(float))
        
    f.close()
    print('matches written')
    offset = offset + head['Ngroups_ThisFile_Redshift']
