#!/usr/bin/python

from multiprocessing import Pool, cpu_count
import numpy as np
import os
import itertools
import time
import sys 

sim = str(sys.argv[1])
subvolume_first_idx = str(sys.argv[2])
out_path = str(sys.argv[3])
sam_path = str(sys.argv[4])
nsubvols = int(sys.argv[5])

subvolumes = np.arange(nsubvols)


def run_gf(INPUT):
    # what isotree
    subvolume = subvolume_first_idx + '_%s_%s' % (INPUT[0], INPUT[1])
    # the folder name for each set of parameters and the matching parameter file name
    subvolume_path = '%s/%s' % (out_path, subvolume)

    # Now run sams in the created directory, using the parameter file we just created.
    os.system('%s/gf %s/param.scsam &> %s/progress.log' % (sam_path, subvolume_path, subvolume_path))


# Create the input file that goes into the module to run the code
INPUT = np.array(list(itertools.product(subvolumes, subvolumes)))

# The number of nodes to use and start the multi-processing
PoolNumber = cpu_count()
pool = Pool(processes=PoolNumber)

# This is where the code is called
out = np.array(pool.map(run_gf, INPUT))

# Close up the multi-processing
pool.close()
