# SAM-Pipeline
Pipeline scripts for running and post-processing the Santa-Cruz Semi-analytic model.
 
## Scripts and Process
...

## Modules and Dependencies
...

##Process Pipeline
###1. Creating isotrees
```
bash/create_isotrees.sh
```

...
###2. Running the SAM
```
bash/submit_sam.sh
--
running/gen_files.py
running/run_SAM_multi.py
```
To clarify terms and definitions in the job submission file: 

**Subvols**: The cube root of the total number of subvolumes. There are 125 subvolumes in TNG100, 125 = 5^3. 

**Partition**: What set of subvolumes of the volume you are running the SAM on. 
Taking TNG100 as example, there are 125 subvolumes labeled [0, 0, 0], [0, 0, 1], ..., [0, 0, 4], [0, 1, 0], 
..., [4, 4, 4]. Partition 0 would mean taking all subvolumes between [0, 0, 0] and [0, 4, 4], partition 1 would
be all subvolumes between [1, 0, 0] and [1, 4, 4], and so on. 

If you plan on re-running the SAM for any reason (parameter variation, updated equations, etc.), then it is 
***highly suggested*** to make your output directory different from your input one.  

The job script begins by removing anything related to that partition's previous runs in the output directory, followed 
by creating a new set of folders for input and output files. For each subvolume in the partition, a parameter file 
(scsam.param) and a list of files to run the SAM on (files.list) are created in their respective directories. After this
set of input files is created, the script finishes by running the SAM on the entire partition. You can monitor the status
of each subvolume through their individual progress.log files if VERBOSE=1 in scsam.param. 

To run on the next partition, simply increment partition to the next one in the set and resubmit the job.
If resources are available, it is possible to modify this script to utilize mpirun or other node multiprocessing tools 
in order to run multiple partitions through a single job request. 

###3. HDF5 Outputs
```
bash/hdf5_sam.sh
--
postprocessing/get-redshifts.py
postprocessing/tree-offsets.py
```
When modifying hdf5_sam.sh, you will need to change the following variables: 
    ```[NSUBVOL, SNAP_RANGE, SCRIPT_PATH, IN_PATH, OUT_PATH]. ```
While ```SIM``` only exists to be inserted into path directories and it is optional if you chose to 
write out ```IN_PATH``` and ```OUT_PATH``` directories in full. Though, it is useful to have especially if you are 
running on different boxes. Similar to before, you will need to note cube root of the total number of subvolumes
as ```NSUBVOL```. 

Instead of working on a partition of the subvolumes, the job postprocesses all ASCII outputs first into hdf5, followed
by creating supplemental files for analysis. First, the output directory is created, and if it already exists, is cleaned
of existing outputs. Each subvolume is then post-processed, creating a **subvolume.hdf5** file in its own directory. 
Galprop and haloprop are loaded as pandas data frames, where there are subsequently cleaned. 
The naming convention and organization of each dataset and field are designed to mimic IllustrisTNG, 
creating a friendly user experience for users that are familiar with Illustris. 

Provided that the supplemental script was not commented out, the following directory structure should be the result:  

``` 
OUT_PATH/
OUT_PATH/output/
	subvolume catalog: OUT_PATH/output/0_0_0/subvolume.hdf5
	merger tree offsets: OUT_PATH/output/0_0_0/tree-offsets.hdf5
	tree lookup file: OUT_PATH/output/lookup/tree_lookup.hdf5
```

###4. Output Verification

###5. Optional Fields and Files


