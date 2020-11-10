#!/usr/bin/python

from multiprocessing import Pool, cpu_count
import numpy as np
import os
import itertools
import time
import sys 

subvolume_first_idx = str(sys.argv[1])
sim = str(sys.argv[2])
base_path = str(sys.argv[3])
nsubvols = int(sys.argv[4])

subvolumes = np.arange(nsubvols)

def run_gf(INPUT):
    sam_path = "%s/sc-sam/gf"%(base_path) 
    
    j, k = INPUT[0], INPUT[1]
    
    # what isotrees 
    rid = subvolume_first_idx + '_%s_%s'%(j, k)
    # the folder name for each set of parameters and the matching parameter file name
    rid_path = '%s/%s/isotrees/%s'%(base_path, sim, rid)
    # the file name of the parameter file
    para_name = 'param.scsam'

    # Now run sams in the created directory, using the parameter file we just created.
    os.system('%s %s/%s &> %s/%s'%(sam_path, rid_path, para_name, rid_path, "progress.log"))

#Create the input file that goes into the module to run the code
INPUT = np.array(list(itertools.product(subvolumes, subvolumes)))

#The number of nodes to use and start the multi-processing
PoolNumber = cpu_count()
pool = Pool(processes = PoolNumber)

#This is where the code is called
out = np.array(pool.map(run_gf, INPUT))

#Close up the multi-processing
pool.close()
