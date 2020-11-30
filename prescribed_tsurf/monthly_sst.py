#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-20.10/bin/python3

import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
import os

## PARSE ARGUMENTS
parser=ArgumentParser()
parser.add_argument('-i','--input',type=str)
parser.add_argument('-o','--output',type=str)
parser.add_argument('--id','--exp_id',type=str)
parser.add_argument('-s','--stream',type=str,default="a")
parser.add_argument('-g','--greb',action='store_true')
args=parser.parse_args()

input_folder=args.input
output_file=args.output
exp_id=args.id
greb=args.greb
if exp_id is None: input_folder,exp_id = os.path.split(input_folder)
stream=args.stream

## SCRIPT
from myfuncs import Constants
import xarray as xr
import numpy as np
from multiprocessing import Pool
from dask.diagnostics import ProgressBar
from cftime import Datetime360Day

os.makedirs(os.path.split(output_file)[0],exist_ok=True)

data=xr.open_mfdataset(os.path.join(input_folder,"{}_p{}*.nc".format(exp_id,stream)),
                       concat_dim="time",parallel=True).surface_temperature
data = data.rename({'longitude_0':'longitude','latitude_0':'latitude'})

land_mask=xr.open_dataarray(Constants.um.land_mask_file())
time=[Datetime360Day(0,m,16,0) for m in np.arange(1,13)]
ref=xr.open_dataarray("/g/data/w48/dm5220/ancil/ref/qrclim.sst_noland.nc").squeeze()

annual_cycle = data.isel(time=slice(-30*12,None)).groupby("time.month").mean('time',keep_attrs=True)
annual_cycle = annual_cycle.rename({'month':'t'}).assign_coords(t=time)

if greb:
    greb_file="/g/data3/w48/dm5220/data/exp_precip_change/ancil/GREB_response.nc"
    g=xr.open_dataarray(greb_file).squeeze()
    g=g.interp(coords={'latitude':annual_cycle.latitude},kwargs={'fill_value':'extrapolate'})
    annual_cycle=(g+annual_cycle)

ts=ref.where(land_mask==1,annual_cycle).astype(np.float32)
ts.attrs['units'] = 'K' ; ts.attrs['long_name'] = 'Surface Temperature' ; ts.name= 'surface_temperature'
del ts['forecast_reference_time'];del ts['surface'];del ts['height']

encoding = {ts.name: {'zlib':True,'shuffle':True,'complevel':4}}
with ProgressBar():
    ts.to_netcdf(output_file,encoding=encoding)
