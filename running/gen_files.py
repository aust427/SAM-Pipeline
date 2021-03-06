import sys

SIM = str(sys.argv[1])
nsubvol = int(sys.argv[2])
m_th = str(sys.argv[3])
partition = int(sys.argv[4])
lib_path = '%s' % str(sys.argv[5])
in_path = '%s' % str(sys.argv[6])
out_path = '%s' % str(sys.argv[7])

# SIM_LIST = {'L35n2160TNG': {'n_subvol': 6, '100m_DM': 0},
#             'L75n1820TNG': {'n_subvol': 5, '100m_DM': '8.85E8'},
#             'L205n2500TNG': {'n_subvol': 7, '100m_DM': '6.98E9'}
#             }


def gen_paramdotscsam(subvolume, filesdotlist, mDM):
    content = '\
#gf parameter file (gfn.v2)\n\
#december 2017\n\
#pathname of input and output\n\
"%s/%s/"\n\
#pathname of library files\n\
"%s/"\n\
#verbosity\n\
1\n\
#seed\n\
-12345\n\
#main free parameters\n\
#chi_gas sigma_crit\n\
1.7 6.0\n\
#tau_star_0\n\
1.0\n\
#recipe for quiescent star formation 0=kenn density 1=bigiel1 2=bigiel2\n\
2\n\
#H2 recipe (0 = GK 1 = KMT 2= BR)\n\
0\n\
#ionized gas\n\
#sigma_HII fion_internal\n\
0.4 0.2\n\
#epsilon_SN_0 alpha_rh f_eject_thresh (km/s)\n\
#gas is ejected if V_halo<f_eject_thresh\n\
1.7 3.0 110.0\n\
#drive_AGN_winds epsilon_wind_QSO\n\
1 0.5\n\
#YIELD f_enrich_cold\n\
1.2 1.0\n\
#cooling enrichment (0=self-consistent 1=fixed) Zh_fixed\n\
0 0.0\n\
#radio heating parameters: f_Edd_radio\n\
2.0E-03\n\
#f_recycle (recycled gas from mass loss/SN)\n\
0.43\n\
#BH parameters\n\
#fbhcrit tau_Q mseedbh\n\
0.5 0.4 0.04 1.0E04\n\
#bhmassbulgemassev\n\
#0=NOEV 1= ZEV 2=FGAS 3=BHFP\n\
1\n\
#sigmaBH_create\n\
0.3\n\
#tidal stripping (0/1)\n\
#if on, expects arguments f_strip tau_strip f_dis\n\
#to make stripping MORE effective make f_strip<1\n\
#to make stripping less effective make f_strip>1\n\
1 1.0 0.22 0.8\n\
#f_scatter\n\
0.2\n\
#f_return (re-infall of ejected gas)\n\
0.1\n\
#SQUELCH z1 z1 z_squelch\n\
#z1 and z2 should be regarded as just parameters in the okamoto fitting fnc\n\
#z_squelch is the redshift that squelching is turned on\n\
1 9.0 3.5 8.0\n\
#disk model 0=SP 1=isothermal 2=MMW\n\
2\n\
#alpha_burst\n\
3.0\n\
#disk instability\n\
#0=off 1=on (stars+gas)\n\
#epsilon_m\n\
1 0.3\n\
#cosmological parameters\n\
#geometry: 0=EDS, 1=FLAT, 2=OPEN\n\
1\n\
#Omega_0 (matter) Omega_Lambda_0 h_100\n\
0.3089 0.6911 0.6774\n\
#f_baryon: negative number means use default value\n\
0.1573\n\
#variance file\n\
"variance/var.planck15.dat"\n\
#save_history\n\
1\n\
#metallicity binning information\n\
#NMET_SFHIST minmet_sfhist maxmet_sfhist\n\
12 -2.5 0.6\n\
#NT_SFHIST dt_sfhist\n\
1381 0.01\n\
#zmin_outputsfhist zmax_outputsfhist mstarmin_outputsfhist [code units]\n\
0.79000 1.80000 10.0\n\
#minimum root mass (Msun)\n\
%s\n\
#tree file format 0=bolshoi planck 1=illustrisTNG\n\
1\n\
#filename of file containing list of tree filenames\n\
"%s"\n\
#output\n\
#NSNAP (number of snapshots in the merger tree file)\n\
100\n\
#NZOUT\n\
1\n\
#minsnap maxsnap must be NZOUT entries (set to 1 NSNAP for NZOUT=1)\n\
0 99\n\
#quantities to output:\n\
#galprop halos history trace mergers\n\
1 1 0 0 0\n\
#GAL_SELECT 0=mstar 1=mhalo\n\
1\n\
%s\n\
#C_rad (major): sp-sp, sp-e, e-e\n\
2.5 0 0\n\
#C_rad (minor): sp-sp, sp-e, e-e\n\
1.35 0 0\n\
#C_int (major): sp-sp, sp-e, e-e\n\
0.5 0.5 0.5\n\
#C_int (minor): sp-sp, sp-e, e-e\n\
0.5 0.5 0.5\n\
#usemainbranchonly (0/1)\n\
0\n\
' % (out_path, subvolume, lib_path, mDM, filesdotlist, mDM)

    with open('%s/%s/param.scsam' % (out_path, subvolume), "w") as f:
        f.write(content)


def gen_filesdotlist(subvolume):
    content = '\
1\n\
"%s/isotree_%s.dat"\n\
' % (in_path, subvolume)
    with open('%s/%s/files.list' % (out_path, subvolume), "w") as f:
        f.write(content)
    return '%s/%s/files.list' % (out_path, subvolume)


for j in range(0, nsubvol):
    for k in range(0, nsubvol):
        filesdotlist = gen_filesdotlist('%s_%i_%i' % (partition, j, k))
        gen_paramdotscsam('%s_%i_%i' % (partition, j, k), filesdotlist, m_th)


