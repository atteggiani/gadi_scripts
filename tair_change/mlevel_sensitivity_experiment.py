#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-20.10/bin/python3

import warnings
warnings.simplefilter("ignore")
import os
import numpy as np
import myfuncs as my
import xarray as xr
from importlib import reload
from cftime import Datetime360Day as dt360
from itertools import tee

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

#Create base xarray with all values equal 0
time = [dt360(0,m,16) for m in range(1,13)]
lat = my.UM.latitude
lon = my.UM.longitude 
levs = my.UM.hybrid_height
coords=(time,levs,lat,lon)
b=np.zeros([len(x) for x in coords],dtype=np.float32)
tac=xr.DataArray(data=b, dims=("time","hybrid_ht","latitude","longitude") ,coords=coords,name="tair_corrections")

ref_levs=[1,8,17,25,38]
lat = np.arange(-90,90+30,30)
levs=[tac.hybrid_ht.values[l-1] for l in ref_levs]
plevs=[1000,850,500,200,20]
coeff=0.003

for l in pairwise(lat):
    for ll,pl in zip(pairwise(levs),pairwise(plevs)):
        cond_lat = np.logical_and(tac.latitude>=l[0],
                                  tac.latitude<=l[1])
        cond_lev = np.logical_and(tac.hybrid_ht>=ll[0],
                                  tac.hybrid_ht<=ll[1])
        cond = ~np.logical_and(cond_lat,cond_lev)
        new_tac=tac.where(cond,coeff)
        
        output_file = "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/sex/files_for_xancil/lat.{}_{}.plev.{}_{}.nc".format(l[0],l[1],pl[0],pl[1])
        encoding = {new_tac.name: {'zlib':True,'shuffle':True,'complevel':4,'chunksizes': [1,8,73,96]}}
        new_tac.to_netcdf(output_file,encoding=encoding)
        print("Created {}".format(os.path.split(output_file)[1]))