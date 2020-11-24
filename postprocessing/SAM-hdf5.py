import numpy as np
import pandas as pd
import h5py
import sys

x_i = int(sys.argv[1])
x_j = int(sys.argv[2])
x_k = int(sys.argv[3])

n_sub = int(sys.argv[4])

sim = sys.argv[5]
input_path = sys.argv[6]
snap_range = str(sys.argv[7])

print('subvolume: %i_%i_%i' % (x_i, x_j, x_k))

g_colnames = ['halo_index', 'birthhaloid', 'roothaloid', 'redshift', 'sat_type',
              'mhalo', 'm_strip', 'rhalo', 'mstar', 'mbulge', 'mstar_merge', 'v_disk',
              'sigma_bulge', 'r_disk', 'r_bulge', 'mcold', 'mHI', 'mH2', 'mHII', 'Metal_star',
              "Metal_cold", 'sfr', 'sfrave20myr', 'sfrave100myr', 'sfrave1gyr',
              'mass_outflow_rate', 'metal_outflow_rate', 'mBH', 'maccdot', 'maccdot_radio',
              'tmerge', 'tmajmerge', 'mu_merge', 't_sat', 'r_fric', 'x_position',
              'y_position', 'z_position', 'vx', 'vy', 'vz']

h_colnames = ['halo_index', 'halo_id', 'roothaloid', 'orig_halo_ID', 'redshift', 'm_vir', 'c_nfw',
              'spin', 'm_hot', 'mstar_diffuse', 'mass_ejected', 'mcooldot',
              'maccdot_pristine', 'maccdot_reaccrete', 'maccdot_metal_reaccrete',
              'maccdot_metal', 'mdot_eject', 'mdot_metal_eject', 'maccdot_radio',
              'Metal_hot', 'Metal_ejected', 'snap_num']

g_header_rows = []
for i in range(0, len(g_colnames)):
    g_header_rows.append(i)

h_header_rows = []
for i in range(0, len(h_colnames)):
    h_header_rows.append(i)

galprop = pd.read_csv(input_path + '/' + sim + '/isotrees/%i_%i_%i/' % (x_i, x_j, x_k)
                      + 'galprop_%s.dat' % snap_range, delimiter=' ', skiprows=g_header_rows, names=g_colnames)
print('galprop read! shape:', galprop.shape)

haloprop = pd.read_csv(input_path + '/' + sim + '/isotrees/%i_%i_%i/' % (x_i, x_j, x_k)
                       + 'haloprop_%s.dat' % snap_range, delimiter=' ', skiprows=h_header_rows, names=h_colnames)
print('haloprop read! shape:', haloprop.shape)

redshifts = h5py.File(input_path + "/redshift.hdf5", "r")['Redshifts'][:]

galprop_n = []
haloprop_n = []

for z in redshifts:
    galprop_n.append(galprop[galprop['redshift'] == z].shape[0])
    haloprop_n.append(haloprop[haloprop['redshift'] == z].shape[0])

group = h5py.File(input_path + '/' + sim + '/outputs/subvolume_%i_%i_%i.hdf5' % (x_i, x_j, x_k), "w")

header = group.create_group("Header")

header.attrs.create('Ngroups_ThisFile', data=haloprop.shape[0], dtype='uint32')
header.attrs.create('Nsubgroups_ThisFile', data=galprop.shape[0], dtype='uint32')
header.attrs.create('Nsubvolumes', data=n_sub ** 3, dtype='int32')

redshift_table = header.create_dataset("Redshifts", (redshifts.shape[0],), dtype='<f8', data=redshifts)

subhalo_table = header.create_dataset('Nsubgroups_ThisFile_Redshift', (len(galprop_n),),
                                      data=np.array(galprop_n), dtype='<i8')

halo_table = header.create_dataset('Ngroups_ThisFile_Redshift', (len(haloprop_n),),
                                   data=np.array(haloprop_n), dtype='<i8')

subhalos = group.create_group("Galprop")

# Velocity & Position 3D 
subhalovel = subhalos.create_dataset("GalpropVel", (galprop.shape[0], 3), dtype='<f4',
                                     data=galprop[['vx', 'vy', 'vz']].values)
subhalopos = subhalos.create_dataset("GalpropPos", (galprop.shape[0], 3), dtype='<f4',
                                     data=galprop[['x_position', 'y_position', 'z_position']].values)

# Radius quantities 
subhaloRhalo = subhalos.create_dataset("GalpropRhalo", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['rhalo'].values)
subhaloRdisk = subhalos.create_dataset("GalpropRdisk", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['r_disk'].values)
subhaloRbulge = subhalos.create_dataset("GalpropRbulge", (galprop.shape[0],),
                                        dtype='<f4', data=galprop['r_bulge'].values)
subhaloRfric = subhalos.create_dataset("GalpropRfric", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['r_fric'].values)

# Metal quantities
subhaloZstar = subhalos.create_dataset("GalpropZstar", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['Metal_star'].values)
subhaloZcold = subhalos.create_dataset("GalpropZcold", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['Metal_cold'].values)

# Mass quantities 
subhaloMhalo = subhalos.create_dataset("GalpropMvir", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['mhalo'].values)
subhaloMstar = subhalos.create_dataset("GalpropMstar", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['mstar'].values)
subhaloMstarMerge = subhalos.create_dataset("GalpropMstar_merge", (galprop.shape[0],),
                                            dtype='<f4', data=galprop['mstar_merge'].values)
subhaloMbulge = subhalos.create_dataset("GalpropMbulge", (galprop.shape[0],),
                                        dtype='<f4', data=galprop['mbulge'].values)
subhaloMHI = subhalos.create_dataset("GalpropMHI", (galprop.shape[0],),
                                     dtype='<f4', data=galprop['mHI'].values)
subhaloMH2 = subhalos.create_dataset("GalpropMH2", (galprop.shape[0],),
                                     dtype='<f4', data=galprop['mH2'].values)
subhaloMHII = subhalos.create_dataset("GalpropMHII", (galprop.shape[0],),
                                      dtype='<f4', data=galprop['mHII'].values)
subhaloMcold = subhalos.create_dataset("GalpropMcold", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['mcold'].values)
subhaloMbh = subhalos.create_dataset("GalpropMBH", (galprop.shape[0],),
                                     dtype='<f4', data=galprop['mBH'].values)
subhaloMstrip = subhalos.create_dataset("GalpropMstrip", (galprop.shape[0],),
                                        dtype='<f4', data=galprop['m_strip'].values)

# BH mass accretion quantities
subhaloMaccdot = subhalos.create_dataset("GalpropMaccdot", (galprop.shape[0],),
                                         dtype='<f4', data=galprop['maccdot'].values)
subhaloMaccdot_radio = subhalos.create_dataset("GalpropMaccdot_radio", (galprop.shape[0],),
                                               dtype='<f4', data=galprop['maccdot_radio'].values)

# Star formation rate quantities
subhaloSfr = subhalos.create_dataset("GalpropSfr", (galprop.shape[0],),
                                     dtype='<f4', data=galprop['sfr'].values)
subhaloSfrave20myr = subhalos.create_dataset("GalpropSfrave20myr", (galprop.shape[0],),
                                             dtype='<f4', data=galprop['sfrave20myr'].values)
subhaloSfrave100myr = subhalos.create_dataset("GalpropSfrave100myr", (galprop.shape[0],),
                                              dtype='<f4', data=galprop['sfrave100myr'].values)
subhaloSfrave1gyr = subhalos.create_dataset("GalpropSfrave1gyr", (galprop.shape[0],),
                                            dtype='<f4', data=galprop['sfrave1gyr'].values)

# merger times
subhaloTmerger = subhalos.create_dataset("GalpropTmerger", (galprop.shape[0],),
                                         dtype='<f4', data=galprop['tmerge'].values)
subhaloTmergermajor = subhalos.create_dataset("GalpropTmerger_major", (galprop.shape[0],),
                                              dtype='<f4', data=galprop['tmajmerge'].values)
subhaloMassRatioMerger = subhalos.create_dataset("GalpropMu_merger", (galprop.shape[0],),
                                                 dtype='<f4', data=galprop['mu_merge'].values)

# outflow rates 
subhaloOutflowMass = subhalos.create_dataset("GalpropOutflowRate_Mass", (galprop.shape[0],),
                                             dtype='<f4', data=galprop['mass_outflow_rate'].values)
subhaloOutflowMetals = subhalos.create_dataset("GalpropOutflowRate_Metal", (galprop.shape[0],),
                                               dtype='<f4', data=galprop['metal_outflow_rate'].values)

# ID quantities 
subhaloHaloprop_idx = subhalos.create_dataset("GalpropHaloIndex", (galprop.shape[0],),
                                              dtype='uint32', data=galprop['halo_index'].values.astype(float))
subhaloBirthHaloID = subhalos.create_dataset("GalpropBirthHaloID", (galprop.shape[0],),
                                             dtype='uint32', data=galprop['birthhaloid'].values.astype(float))
subhaloRootHaloID = subhalos.create_dataset("GalpropRootHaloID", (galprop.shape[0],),
                                            dtype='uint32', data=galprop['roothaloid'].values.astype(float))

# Misc 
subhaloRedshift = subhalos.create_dataset("GalpropRedshift", (galprop.shape[0],),
                                          dtype='<f4', data=galprop['redshift'].values)

subhaloSatType = subhalos.create_dataset("GalpropSatType", (galprop.shape[0],),
                                         dtype='<f4', data=galprop['sat_type'].values)

subhaloVdisk = subhalos.create_dataset("GalpropVdisk", (galprop.shape[0],),
                                       dtype='<f4', data=galprop['v_disk'].values)

subhaloSigmaBulge = subhalos.create_dataset("GalpropSigmaBulge", (galprop.shape[0],),
                                            dtype='<f4', data=galprop['sigma_bulge'].values)

subhaloTsat = subhalos.create_dataset("GalpropTsat", (galprop.shape[0],),
                                      dtype='<f4', data=galprop['t_sat'].values)

groups = group.create_group("Haloprop")

# mass accretion quantities
groupMaccdot_radio = groups.create_dataset("HalopropMaccdot_radio", (haloprop.shape[0],), dtype='<f4',
                                           data=haloprop['maccdot_radio'].values)
groupMcooldot = groups.create_dataset("HalopropMcooldot", (haloprop.shape[0],),
                                      dtype='<f4', data=haloprop['mcooldot'].values)
groupMaccdot_metal = groups.create_dataset("HalopropMaccdot_metal", (haloprop.shape[0],),
                                           dtype='<f4', data=haloprop['maccdot_metal'].values)
groupMaccdot_pristine = groups.create_dataset("HalopropMaccdot_pristine", (haloprop.shape[0],),
                                              dtype='<f4', data=haloprop['maccdot_pristine'].values)

# reaccretion quantities
groupMaccdot_reaccreate = groups.create_dataset("HalopropMaccdot_reaccreate", (haloprop.shape[0],),
                                                dtype='<f4', data=haloprop['maccdot_reaccrete'].values)
groupMaccdot_reaccreate_metal = groups.create_dataset("HalopropMaccdot_reaccreate_metal", (haloprop.shape[0],),
                                                      dtype='<f4', data=haloprop['maccdot_metal_reaccrete'].values)

# ejection quantities
groupMdot_eject = groups.create_dataset("HalopropMdot_eject", (haloprop.shape[0],),
                                        dtype='<f4', data=haloprop['mdot_eject'].values)
groupMdot_eject_metal = groups.create_dataset("HalopropMdot_eject_metal", (haloprop.shape[0],),
                                              dtype='<f4', data=haloprop['mdot_metal_eject'].values)
groupMass_eject = groups.create_dataset("HalopropMass_ejected", (haloprop.shape[0],),
                                        dtype='<f4', data=haloprop['mass_ejected'].values)
groupMetal_eject = groups.create_dataset("HalopropMetal_ejected", (haloprop.shape[0],),
                                         dtype='<f4', data=haloprop['Metal_ejected'].values)

# CGM quantities
groupHotMass = groups.create_dataset("HalopropMhot", (haloprop.shape[0],),
                                     dtype='<f4', data=haloprop['m_hot'].values)
groupHotMetal = groups.create_dataset("HalopropZhot", (haloprop.shape[0],),
                                      dtype='<f4', data=haloprop['Metal_hot'].values)

# ID quantities
groupIndex = groups.create_dataset("HalopropIndex", (haloprop.shape[0],),
                                   dtype='uint32', data=haloprop['halo_index'].values.astype(float))
groupHaloid = groups.create_dataset("HalopropHaloID", (haloprop.shape[0],),
                                    dtype='uint32', data=haloprop['halo_id'].values.astype(float))
groupRoothaloid = groups.create_dataset("HalopropRootHaloID", (haloprop.shape[0],),
                                        dtype='uint32', data=haloprop['roothaloid'].values.astype(float))
groupRockstarid = groups.create_dataset("HalopropRockstarHaloID", (haloprop.shape[0],),
                                        dtype='uint32', data=haloprop['orig_halo_ID'].values.astype(float))

# misc quantities
groupRedshift = groups.create_dataset("HalopropRedshift", (haloprop.shape[0],),
                                      dtype='<f4', data=haloprop['redshift'].values)
groupSnapNum = groups.create_dataset("HalopropSnapNum", (haloprop.shape[0],),
                                     dtype='<f4', data=haloprop['snap_num'].values)

groupcNFW = groups.create_dataset("HalopropC_nfw", (haloprop.shape[0],),
                                  dtype='<f4', data=haloprop['c_nfw'].values)

groupMvir = groups.create_dataset("HalopropMvir", (haloprop.shape[0],),
                                  dtype='<f4', data=haloprop['m_vir'].values)

groupSpin = groups.create_dataset("HalopropSpin", (haloprop.shape[0],),
                                  dtype='<f4', data=haloprop['spin'].values)

groupMstarDiffuse = groups.create_dataset("HalopropMstar_diffuse", (haloprop.shape[0],),
                                          dtype='<f4', data=haloprop['mstar_diffuse'].values)

group.close()
