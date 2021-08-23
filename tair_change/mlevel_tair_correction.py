#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-21.04/bin/python3

import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
import os
import numpy as np
import myfuncs as my
import xarray as xr
from importlib import reload
from cftime import Datetime360Day as dt360
from itertools import tee
import matplotlib.pyplot as plt

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_tac_sex_filename(id):
    tac_folder="/g/data/w48/dm5220/ancil/user_mlevel/tair_change/sex"
    return os.readlink(os.path.join(tac_folder,id))

ind_levs=[1,8,17,25,38]
ref_lat = np.arange(-90,90+30,30)
ref_levs=[my.UM.hybrid_height[l-1] for l in ind_levs]
sex_order=[21,24,23,22,13,16,15,14,5,8,7,6,1,4,3,2,9,12,11,10,17,20,19,18]
sex_names=["sex{}".format(n) for n in sex_order]
sex_args=["s{}".format(n) for n in sex_order]
plevs=[1000,850,500,200,20]

## PARSE ARGUMENTS
parser=ArgumentParser()
parser.add_argument('-o','--output',type=str)
parser.add_argument('-c','--change',type=np.float,default=0)
for arg in sex_args:
    parser.add_argument('-{}'.format(arg),type=np.float)
args=parser.parse_args()

out_file=args.output
change=args.change
change_sex=[eval("args.{}".format(arg)) for arg in sex_args]

#Create base xarray with all values equal 0
time = [dt360(0,m,16) for m in range(1,13)]

lat = my.UM.latitude
lon = my.UM.longitude 
levs = my.UM.hybrid_height
coords=(time,levs,lat,lon)
b=np.zeros([len(x) for x in coords],dtype=np.float32)
tac=xr.DataArray(data=b, dims=("time","hybrid_ht","latitude","longitude") ,coords=coords,name="tair_corrections")
tac+=change
count=0
for l in pairwise(ref_lat):
    for ll,pl in zip(pairwise(ref_levs),pairwise(plevs)):
        if change_sex[count] is not None:
            cond_lat = np.logical_and(tac.latitude>=l[0],
                                    tac.latitude<=l[1])
            cond_lev = np.logical_and(tac.hybrid_ht>=ll[0],
                                    tac.hybrid_ht<=ll[1])
            cond = ~np.logical_and(cond_lat,cond_lev)
            tac=tac.where(cond,change_sex[count])
        count+=1

output_file = "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/files_for_xancil/{}.nc".format(out_file)
encoding = {tac.name: {'zlib':True,'shuffle':True,'complevel':4,'chunksizes': [1,8,73,96]}}
tac.to_netcdf(output_file,encoding=encoding)

