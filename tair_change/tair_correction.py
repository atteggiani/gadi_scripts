import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
from importlib import reload
from cftime import Datetime360Day as dt360
import numpy as np
from dask.diagnostics import ProgressBar

# import os
# import matplotlib.pyplot as plt
# ref=xr.open_dataarray("/g/data3/w48/dm5220/tair_no_corr.nc")

#Create base xarray with all values equal 0
time = [dt360(0,m,16) for m in range(1,13)]
lat = my.Constants.um.latitude
lon = my.Constants.um.longitude 
levs = my.Constants.um.hybrid_height
coords=(time,levs,lat,lon)
b=np.zeros([len(x) for x in coords],dtype=np.float32)
tac=xr.DataArray(data=b, dims=("time","hybrid_ht","latitude","longitude") ,coords=coords,name="tair_corrections")

tac[:,1:2,...] = -0.03
tac[:,3,...] = -0.015
tac[:,5,...] = 0.05
tac[:,6:8,...] = 0.12
tac[:,9:11,...] = 0.06
tac[:,12:17,...] = 0.03
tac[:,18:25,...] = 0.05

output_file = "/g/data/w48/dm5220/scripts/tair_change/test_chen.nc"
encoding = {tac.name: {'zlib':True,'shuffle':True,'complevel':4,'chunksizes': [1,8,73,96]}}
with ProgressBar():
    tac.to_netcdf(output_file,encoding=encoding)