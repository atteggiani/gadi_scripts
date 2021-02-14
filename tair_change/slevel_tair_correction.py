#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-20.10/bin/python3
import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
import os
import myfuncs as my
import xarray as xr
import numpy as np
from cftime import Datetime360Day
import pandas as pd
from datetime import timedelta

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str)
parser.add_argument('-o','--output',type=str)
parser.add_argument('--slab',action='store_true')
args=parser.parse_args()

input_folder=args.input
output_file=args.output
slab=args.slab

def create_flux(t):
    #CREATE QFLUX from ref qflux
    newt=xr.cftime_range(start='0000', periods=12*30*24*3, freq="1H", calendar="360_day")
    oldt=[x+timedelta(days=15) for x in xr.cftime_range(start='0000', periods=36, freq="MS", calendar="360_day")]
    d=xr.open_dataarray("/g/data/w48/dm5220/ancil/qflux/slab-qflux.nc")
    out=np.repeat(d,30*24,axis=0).assign_coords({"t":t})
    out.name="qflux"
    output_file = "/g/data/w48/dm5220/ancil/user_slevel/tair_change/files_for_xancil/qflux_tac.nc"
    encoding = {out.name: {'zlib':True,'shuffle':True,'complevel':4}}
    out.to_netcdf(output_file,encoding=encoding)

def create_mask(t):
    # CREATE LAND MASK from ref land_mask file
    m=xr.open_dataarray("/g/data/w48/dm5220/ancil/land_mask/land_mask.nc")
    newm=m.expand_dims({"t":t})
    if not slab: newm=(newm*0)+1
    output_file = "/g/data/w48/dm5220/ancil/user_slevel/tair_change/files_for_xancil/land_mask_tac.nc"
    encoding = {newm.name: {'zlib':True,'shuffle':True,'complevel':4}}
    newm.to_netcdf(output_file,encoding=encoding)

def create_tsurf(t):
    if input_folder is None:
        ts=xr.DataArray(data=np.zeros((len(t),len(my.Constants.um.latitude),len(my.Constants.um.longitude))),
                                       dims=("time","latitude","longitude"),
                                       coords=(t,my.Constants.um.latitude,my.Constants.um.longitude))
    else:
        data=xr.open_mfdataset(os.path.join(input_folder,"*_pe*.nc"),chunks={"time":1000},
                            combine='nested', concat_dim="time", parallel=True, decode_times=False).surface_temperature
        
        hours_per_year = 360 * 24
        year = 1970 + (data.time-0.5) // hours_per_year
        hour_of_year = data.time % hours_per_year
        time_mi = pd.MultiIndex.from_arrays((year.values, hour_of_year.values), names=('year','h_year'))
        data.coords['time'] = time_mi
        annual_cycle = data.unstack('time').isel(year=slice(-30,None),h_year=slice(0,None,2)).mean('year').rename({'h_year':'time'}).assign_coords(time=t)
        land_mask=xr.open_dataarray(my.Constants.um.land_mask_file())
        ts=annual_cycle.where(land_mask==1,0).astype(np.float32)
        ts.attrs['units'] = 'K' ; ts.attrs['long_name'] = 'Surface Temperature'

    ts.name='tsurf'
    encoding = {ts.name: {'zlib':True,'shuffle':True,'complevel':4}}
    ts.to_netcdf(os.path.join(output_file),encoding=encoding)

time_out=xr.cftime_range(start='0000', periods=12*30*24, freq="1H", calendar="360_day")
# create_flux(time_out)
# create_mask(time_out)
create_tsurf(time_out)
