#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-20.10/bin/python3

import myfuncs as my
import xarray as xr
import numpy as np
from dask.diagnostics import ProgressBar
from cftime import Datetime360Day
import pandas as pd
from datetime import timedelta

def create_flux(time):
    #CREATE QFLUX from ref qflux
    newt=xr.cftime_range(start='0000', periods=12*30*24*3, freq="1H", calendar="360_day")
    oldt=[x+timedelta(days=15) for x in xr.cftime_range(start='0000', periods=36, freq="MS", calendar="360_day")]

    d=xr.open_dataarray("/g/data/w48/dm5220/ancil/qflux/slab-qflux.nc")
    new=xr.apply_ufunc(lambda x: np.tile(x,(1,1,3)),d,input_core_dims=[['t']],exclude_dims={('t')},output_core_dims=[('t')])

    newd=new.assign_coords({"t":oldt})
    intd=newd.interp(t=newt,method="cubic",kwargs={"fill_value": "extrapolate"})

    out=intd.sel(t=slice("0001-01-01","0001-12-30")).assign_coords({"t":time})

    output_file = "/g/data/w48/dm5220/ancil/user_slevel/tair_change/qflux_tair_change.nc"
    encoding = {out.name: {'zlib':True,'shuffle':True,'complevel':4}}
    out.to_netcdf(output_file,encoding=encoding)
def create_mask(time):
    # CREATE LAND MASK from ref land_mask file
    m=xr.open_dataarray("/g/data/w48/dm5220/ancil/land_mask/land_mask.nc")
    newm=m.expand_dims({"t":time})

    output_file = "/g/data/w48/dm5220/ancil/user_slevel/tair_change/land_mask_tair_change.nc"
    encoding = {newm.name: {'zlib':True,'shuffle':True,'complevel':4}}
    newm.to_netcdf(output_file,encoding=encoding)
def create_tsurf(time):
    #CREATE TSURF
    ts=xr.DataArray(np.zeros((12*30*24,73,96)),dims=("t","latitude","longitude"),coords=(time,my.Constants.um.latitude,my.Constants.um.longitude),name="tsurf")

    output_file = "/g/data/w48/dm5220/ancil/user_slevel/tair_change/tsurf_tair_change.nc"
    encoding = {ts.name: {'zlib':True,'shuffle':True,'complevel':4}}
    ts.to_netcdf(output_file,encoding=encoding)

time=xr.cftime_range(start='0000', periods=12*30*24, freq="1H", calendar="360_day")

# create_flux(time)
# create_mask(time)
create_tsurf(time)