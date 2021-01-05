import sys
import site
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import h5py

sys.path.append('/home/agabrielpillai/.local/lib/python3.6/site-packages/')
site.addsitedir('/home/agabrielpillai/') 
site.addsitedir('/home/agabrielpillai/scripts/')

import illustris_python as il
import illustris_sam as ilsam

basePathTNG = str(sys.argv[1])
basePathSAM = str(sys.argv[2])
basePathTNG_DM = str(sys.argv[3])
basePathTNG_RS = str(sys.argv[4])
match_file_path= str(sys.argv[5]) #'/mnt/home/agabrielpillai/ceph/IllustrisTNG/L75n1820TNG_DM/output/postprocessing/rockstar/matching'

matchOutPath = str(sys.argv[6])
imgPath = str(sys.argv[7])

snapStart = int(sys.argv[8])
nsubvol = int(sys.argv[9])

DMO_match = h5py.File('{}/rockstar_subhalo_matching_to_DM.hdf5'.format(match_file_path), 'r')  
FP_match = h5py.File('{}/rockstar_subhalo_matching_to_FP.hdf5'.format(match_file_path), 'r')

f_FP = h5py.File(matchOutPath + '/matches_FP.hdf5', 'w')
FP_G = f_FP.create_group("Subfind")
FP_H = f_FP.create_group("FoF")

f_DM = h5py.File(matchOutPath + '/matches_DM.hdf5', 'w')
DM_G = f_DM.create_group("Subfind")
DM_H = f_DM.create_group("FoF")

def genParams(ax, func, bounds, sam, tng):
    params_1 = func(ax, bounds, sam, tng, 2)
    f = drawHeatmap(ax, params_1[0], params_1[1], params_1[2], 'gray')
    return(params_1)


def drawHeatmap(ax, heatmap, extent, bounds, col_map):
    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])

    f = ax.imshow(heatmap, extent=extent, origin='lower', aspect='auto', cmap=col_map, interpolation='nearest')
    cb = plt.colorbar(f, ax=ax)
    cb.set_label('$log_{10}counts$')
    return(heatmap)


def genHeatmap(ax, q1, q2, bounds):
    heatmap, xedges, yedges = np.histogram2d(q1, q2, range=bounds, bins = (200, 200))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    heatmap = np.log10(heatmap.T)
    return [heatmap, extent, bounds]


def m200_compare_2(ax, bounds, sam, tng, n):
    th = bounds[0][0]

    s = np.log10(sam['mhalo'] * 1e9)
    t = np.log10(1e10*tng['mhalo'] / 0.6674)

    dif = t - s

    return genHeatmap(ax, s, dif, bounds)


def genTNGDF(basePath, snapNum):
    subhalos = il.groupcat.loadSubhalos(basePath, snapNum, fields=['SubhaloGrNr', 'SubhaloPos'])
    group = il.groupcat.loadHalos(basePath, snapNum, fields=['Group_M_TopHat200', 'GroupFirstSub', 'Group_R_TopHat200'])

    tng_hydro = pd.DataFrame()
    tng_hydro['x'] = subhalos['SubhaloPos'][:,0]
    tng_hydro['y'] = subhalos['SubhaloPos'][:,1]
    tng_hydro['z'] = subhalos['SubhaloPos'][:,2]
    tng_hydro['host_idx'] = subhalos['SubhaloGrNr']
    tng_hydro['mhalo'] = group['Group_M_TopHat200'][subhalos['SubhaloGrNr']]
    tng_hydro['rhalo'] = group['Group_R_TopHat200'][subhalos['SubhaloGrNr']]
    tng_hydro = tng_hydro.reset_index(drop=False)
    tng_hydro['central'] = False
    tng_hydro['central'].iloc[group['GroupFirstSub'][group['GroupFirstSub'] != -1]] = True
    
    return tng_hydro


def genMatches(match_file, snapNum, rockstar, tng):
    # will later change to just the full file ...
    match_df = pd.DataFrame()
    match_df['rockstar-idx'] = match_file['Snapshot_{}'.format(snapNum)]['SubhaloIndexDarkRockstar_SubLink'][:]
    match_df = match_df.reset_index(drop=False)
    match_df = match_df.rename(columns={"index": "subfind-idx"})
                          
    match_df = match_df[match_df['rockstar-idx'] != -1].reset_index(drop=True)
    match_df['Rockstar-ID'] = rockstar.iloc[match_df['rockstar-idx']]['Subhalo_ID'].values
    match_df['tng-central'] = tng.iloc[match_df['subfind-idx']]['central'].values
    match_df['tng-host-idx'] = tng.iloc[match_df['subfind-idx']]['host_idx'].values
    match_df = match_df[match_df['tng-central']].reset_index(drop=True).drop(['tng-central'], axis=1)
    match_df['haloprop-idx'] = rockstar.iloc[match_df['rockstar-idx']]['haloprop-idx'].values
    match_df = match_df[match_df['haloprop-idx'] != -1].reset_index(drop=True)
                          
    return match_df

                          
def appendMatches(match_type, haloprop, tng, matches):
    haloprop['subfind_id'] = -1 
    haloprop['fof_id'] = -1 
    haloprop.loc[matches['haloprop-idx'], 'subfind_id'] = matches['subfind-idx'].values
    haloprop.loc[matches['haloprop-idx'], 'fof_id'] = matches['tng-host-idx'].values

    SAM_test = haloprop.iloc[matches['haloprop-idx']].reset_index(drop=True)
    tng_sub = tng.iloc[matches['subfind-idx']].reset_index(drop=True)

    plt.style.use('default')

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    bounds = [[8, 15], [-1.5, 1.5]]
    maps = genParams(ax, m200_compare_2, bounds, SAM_test, tng_sub)
    #fig.show()

    ax.set_xlabel('$log_{10} m_{vir, SAM}$ $[M_{\odot}$]')
    ax.set_ylabel('$log_{10} m_{200, TNG ('+match_type+')} - log_{10} m_{vir, SAM}$ $[M_{\odot}]$')
    plt.savefig(imgPath + '/'+ match_type + '/' + str(snapNum) + '.png', dpi = 300)

    return haloprop


for snapNum in range(snapStart, 100):
    tng_hydro = genTNGDF(basePathTNG, snapNum)
    tng_hydro_DM = genTNGDF(basePathTNG_DM, snapNum)

    subvolume_list = []

    for i in range(nsubvol):
        for j in range(nsubvol):
            for k in range(nsubvol):
                subvolume_list.append([i, j, k])

    # subvolume_list = [[0, 0, 0]]

    haloprop = ilsam.groupcat.load_snapshot_halos(basePathSAM, snapNum, subvolume_list,
                                                  fields=['HalopropRockstarHaloID', 'HalopropMvir', 'HalopropSnapNum'])
    SAM_haloprop = pd.DataFrame()
    SAM_haloprop['orig_halo_ID'] = haloprop['HalopropRockstarHaloID']
    SAM_haloprop['mhalo'] = haloprop['HalopropMvir']
    SAM_haloprop = SAM_haloprop.reset_index(drop=False)
    SAM_haloprop = SAM_haloprop.rename(columns={"index": "halo_index"})

    rockstar = il.groupcat.loadSubhalos(basePathTNG_RS + '/postprocessing/rockstar', snapNum,
                                        fields=['Subhalo_ID', 'SubhaloMassType', 'Subhalo_Rvir'])
    rockstar_df = pd.DataFrame()
    rockstar_df['Subhalo_ID'] = rockstar['Subhalo_ID']
    rockstar_df['mvir'] = rockstar['SubhaloMassType'][:, 1]
    rockstar_df['rvir'] = rockstar['Subhalo_Rvir']

    SAM_sub = SAM_haloprop[['halo_index', 'orig_halo_ID']].sort_values(by='orig_halo_ID')
    SAM_sub = SAM_sub[SAM_sub['orig_halo_ID'].isin(rockstar_df['Subhalo_ID'])]

    rockstar_df = rockstar_df.sort_values(by='Subhalo_ID').reset_index(drop=False)
    rockstar_df['haloprop-idx'] = -1
    rockstar_df.loc[SAM_sub['orig_halo_ID'], 'haloprop-idx'] = SAM_sub['halo_index'].values
    rockstar_df = rockstar_df.sort_values(by='index').reset_index(drop=True)

    match_df_DM = genMatches(DMO_match, snapNum, rockstar_df, tng_hydro_DM)
    SAM_haloprop_DM = appendMatches('DM', SAM_haloprop, tng_hydro_DM, match_df_DM)
    match_snap_DM_1 = FP_G.create_dataset(str(snapNum), (SAM_haloprop_DM.shape[0],),
                                          dtype='int32', data=SAM_haloprop_DM['subfind_id'].values.astype(float))
    match_snap_DM_2 = FP_H.create_dataset(str(snapNum), (SAM_haloprop_DM.shape[0],),
                                          dtype='int32', data=SAM_haloprop_DM['fof_id'].values.astype(float))

    match_df_FP = genMatches(FP_match, snapNum, rockstar_df, tng_hydro)
    SAM_haloprop_FP = appendMatches('FP', SAM_haloprop, tng_hydro, match_df_FP)
    match_snap_FP_1 = DM_G.create_dataset(str(snapNum), (SAM_haloprop_FP.shape[0],),
                                          dtype='int32', data=SAM_haloprop_FP['subfind_id'].values.astype(float))
    match_snap_FP_2 = DM_H.create_dataset(str(snapNum), (SAM_haloprop_FP.shape[0],),
                                          dtype='int32', data=SAM_haloprop_FP['fof_id'].values.astype(float))


f_FP.close()
f_DM.close()
