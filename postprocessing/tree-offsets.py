import site
import sys

sys.path.append('/mnt/home/agabrielpillai/.local/lib/python3.6/site-packages/')
site.addsitedir('/mnt/home/agabrielpillai/scripts/') 
import illustris_sam as ilsam
import numpy as np
import pandas as pd
import h5py 

n_sub = int(sys.argv[1])
sim = sys.argv[2]
input_path = sys.argv[3]

basePathSAM = input_path + '/' + sim + '/'

subvolume_list = []

for i in range(0, n_sub):
    for j in range(0, n_sub):
        for k in range(0, n_sub):
            subvolume_list.append([i, j, k])

n_entries = []

base_df = pd.DataFrame(columns=['RootHaloID', 'Mvir', 'Subvolume', 
                                'gal_start', 'gal_end', 'halo_start', 'halo_end'])

for subvolume in subvolume_list:
    galprop = ilsam.groupcat.load_galprop(basePathSAM, subvolume,
                                          fields=['GalpropRootHaloID'])
    haloprop = ilsam.groupcat.load_haloprop(basePathSAM, subvolume,
                                            fields=['HalopropRootHaloID'])
    root_halos = ilsam.groupcat.load_snapshot_halos(basePathSAM, 99, [subvolume],
                                                    fields=['HalopropRootHaloID', 'HalopropMvir'])
    
    subvolume_df = pd.DataFrame(columns=['RootHaloID', 'Mvir', 'Subvolume', 
                                         'LenGalpropIdxs', 'LenHalopropIdxs'])
    subvolume_df['RootHaloID'] = root_halos['HalopropRootHaloID'][:]
    subvolume_df['Mvir'] = root_halos['HalopropMvir'][:]
    subvolume_df['Subvolume'] = [subvolume] * subvolume_df.shape[0]
    
    g_list = []
    h_list = []
    n_entries.append(subvolume_df['RootHaloID'].shape[0])

    for i in range(0, subvolume_df.shape[0]):
        g_list.append(list(np.where(galprop['GalpropRootHaloID'] == subvolume_df['RootHaloID'][i]))[0])
        h_list.append(list(np.where(haloprop['HalopropRootHaloID'] == subvolume_df['RootHaloID'][i]))[0])

    offset = h5py.File(basePathSAM + 'postprocessing/tree_offsets/offsets_%i_%i_%i.hdf5'
                       % (subvolume[0], subvolume[1], subvolume[2]), "w")
    offsets = offset.create_group("Offsets")
    
    subvolume_df['LenGalpropIdxs'] = [len(li) for li in g_list]
    subvolume_df['gal_start'] = 0
    subvolume_df['gal_end'] = 0
    subvolume_df['gal_start'][1:] = np.cumsum(subvolume_df['LenGalpropIdxs'][:-1])
    subvolume_df['gal_end'][:] = np.cumsum(subvolume_df['LenGalpropIdxs']) 
    g_list = [item for sublist in g_list for item in sublist]
    galprop_offsets = offsets.create_dataset("GalpropOffsets", (len(g_list),), dtype='uint32', data=g_list)
    
    subvolume_df['LenHalopropIdxs'] = [len(li) for li in h_list]
    subvolume_df['halo_start'] = 0
    subvolume_df['halo_end'] = 0
    subvolume_df['halo_start'][1:] = np.cumsum(subvolume_df['LenHalopropIdxs'][:-1])
    subvolume_df['halo_end'][:] = np.cumsum(subvolume_df['LenHalopropIdxs']) 
    h_list = [item for sublist in h_list for item in sublist]
    haloprop_offsets = offsets.create_dataset("HalopropOffsets", (len(h_list),), dtype='uint32', data=h_list)
    
    offset.close()
        
    base_df = pd.concat([base_df, subvolume_df.drop(['LenGalpropIdxs', 'LenHalopropIdxs'], axis=1)])
    

table_offsets = np.zeros([len(subvolume_list), 2])
table_offsets[:, 1] = np.cumsum(n_entries)
table_offsets[1:, 0] = np.cumsum(n_entries[:-1])

lookup = h5py.File(basePathSAM + 'postprocessing/tree_offsets/offsets_lookup.hdf5', 'w') 

table2 = lookup.create_group("Lookup_Lookup")
Subvolume = table2.create_dataset("Subvolume", (len(subvolume_list), 3), 
                                  dtype='int', data=np.array(subvolume_list))
offsets = table2.create_dataset("Offsets", table_offsets.shape,
                                dtype='uint32', data=table_offsets)

table = lookup.create_group("Lookup_Table")
RootHaloID = table.create_dataset("RootHaloID", (base_df.shape[0], ), 
                                  dtype='uint32', data=base_df['RootHaloID'].values.astype(float))
Subvolume = table.create_dataset("Subvolume", (base_df.shape[0], 3), 
                                 dtype='int', data=np.array([x for x in base_df['Subvolume'].values]))
gal_idxs = table.create_dataset("GalpropOffsets", (base_df.shape[0], 2), 
                                dtype='uint32', data=base_df[['gal_start', 'gal_end']].values.astype(float))
halo_idxs = table.create_dataset("HalopropOffsets", (base_df.shape[0], 2), 
                                 dtype='uint32', data=base_df[['halo_start', 'halo_end']].values.astype(float))

lookup.close()
