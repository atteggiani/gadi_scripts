#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-21.04/bin/python3

import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
import os

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str)
parser.add_argument('-o','--output',type=str)
parser.add_argument('--id','--exp_id',type=str)
parser.add_argument('-s','--stream',type=str,default="c")
parser.add_argument('-g','--greb',action='store_true')
args=parser.parse_args()

input_folder=args.input
output_file=args.output
exp_id=args.id
stream=args.stream
greb=args.greb
if exp_id is None: input_folder,exp_id = os.path.split(input_folder)

from myfuncs import UM
import xarray as xr
import numpy as np
from dask.diagnostics import ProgressBar
from cftime import Datetime360Day
import pandas as pd

os.makedirs(os.path.split(output_file)[0],exist_ok=True)

data=xr.open_mfdataset(os.path.join(input_folder,"{}_p{}*.nc".format(exp_id,stream)),
                       combine='nested', concat_dim="time", parallel=True, decode_times=False).chunk({'time':40000}).surface_temperature

hours_per_year = 360 * 24
year = 1970 + data.time // hours_per_year ; year[-1]=year[0]
hour_of_year = data.time % hours_per_year
time_mi = pd.MultiIndex.from_arrays((year, hour_of_year), names=('year','h_year'))

time=np.roll(xr.cftime_range(start='0000', periods=2880, freq="3H", calendar="360_day"),-1)

data.coords['time'] = time_mi

annual_cycle = data.unstack('time').isel(year=slice(-30,None)).mean('year').rename({'h_year':'time'}).roll(time=-1).assign_coords(time=time)
if greb:
    greb_file="/g/data3/w48/dm5220/data/ancil/GREB_response.nc"
    g=xr.open_dataarray(greb_file).squeeze()
    g=g.interp(coords={'latitude':annual_cycle.latitude},kwargs={'fill_value':'extrapolate'})
    annual_cycle=(g+annual_cycle)

land_mask=xr.open_dataarray(UM.land_mask_file())
ts=annual_cycle.where(land_mask==1,0).chunk({'time':1})
del ts["surface"]; del ts['t']
ts.attrs['units'] = 'K' ; ts.attrs['long_name'] = 'Surface Temperature' ; ts.name='surface_temperature'

ts=ts.expand_dims({'hybrid_ht':UM.hybrid_height}).transpose('time','hybrid_ht','latitude','longitude').astype(np.float32)

encoding = {ts.name: {'zlib':True,'shuffle':True,'complevel':4,'chunksizes': [1,8,73,96]}}
with ProgressBar():
    ts.to_netcdf(output_file,encoding=encoding)
