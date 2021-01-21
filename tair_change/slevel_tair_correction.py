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

def create_flux(time):
    #CREATE QFLUX from ref qflux
    newt=xr.cftime_range(start='0000', periods=12*30*24*3, freq="1H", calendar="360_day")
    oldt=[x+timedelta(days=15) for x in xr.cftime_range(start='0000', periods=36, freq="MS", calendar="360_day")]
    d=xr.open_dataarray("/g/data/w48/dm5220/ancil/qflux/slab-qflux.nc")
    
    new=xr.apply_ufunc(lambda x: np.tile(x,(1,1,3)),d,input_core_dims=[['t']],exclude_dims={('t')},output_core_dims=[('t')])
    newd=new.assign_coords({"t":oldt})
    intd=newd.interp(t=newt,method="linear",kwargs={"fill_value": "extrapolate"})
    out=intd.sel(t=slice("0001-01-01","0001-12-30")).assign_coords({"t":time})

    # out=np.repeat(d,30*24,axis=0).assign_coords({"t":time})
    output_file = "/g/data/w48/dm5220/ancil/user_slevel/tair_change/files_for_xancil/qflux_tair_change.nc"
    encoding = {out.name: {'zlib':True,'shuffle':True,'complevel':4}}
    out.to_netcdf(output_file,encoding=encoding)

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str)
parser.add_argument('-o','--output',type=str)
parser.add_argument('-s','--stream',type=str,default="c")
parser.add_argument('-g','--greb',action='store_true')
args=parser.parse_args()

input_folder=args.input
output_file=args.output
stream=args.stream
greb=args.greb

time_out=xr.cftime_range(start='0000', periods=12*30*24, freq="1H", calendar="360_day")

data=xr.open_mfdataset(os.path.join(input_folder,"*_p{}*.nc".format(stream)),
                       combine='nested', concat_dim="time", parallel=True, decode_times=False).surface_temperature

hours_per_year = 360 * 24
year = 1970 + data.time // hours_per_year ; year[-1]=year[0]
hour_of_year = data.time % hours_per_year
time_mi = pd.MultiIndex.from_arrays((year.values, hour_of_year.values), names=('year','h_year'))
time=np.roll(xr.cftime_range(start='0000', periods=2880, freq="3H", calendar="360_day"),-1)
data.coords['time'] = time_mi
annual_cycle = data.unstack('time').isel(year=slice(-30,None)).mean('year').rename({'h_year':'time'}).roll(time=-1).assign_coords(time=time)
if greb:
    greb_file="/g/data3/w48/dm5220/data/ancil/GREB_response.nc"
    g=xr.open_dataarray(greb_file).squeeze()
    g=g.interp(coords={'latitude':annual_cycle.latitude},kwargs={'fill_value':'extrapolate'})
    annual_cycle=(g+annual_cycle)

land_mask=xr.open_dataarray(my.Constants.um.land_mask_file())
ts=annual_cycle.where(land_mask==1,0).astype(np.float32)
ts=np.repeat(ts,3,axis=2).assign_coords({"time":time_out})
ts.attrs['units'] = 'K' ; ts.attrs['long_name'] = 'Surface Temperature' ; ts.name='tsurf'

encoding = {ts.name: {'zlib':True,'shuffle':True,'complevel':4}}
ts.to_netcdf(os.path.join(output_file),encoding=encoding)

# create_flux(time_out)