import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
import os

## PARSE ARGUMENTS
parser=ArgumentParser()
parser.add_argument('-i','--input',type=str)
parser.add_argument('-o','--output',type=str)
args=parser.parse_args()

input_folder=args.input
output_file=args.output

## SCRIPT
import myfuncs as my
import xarray as xr
import numpy as np
from multiprocessing import Pool
from dask.diagnostics import ProgressBar
from cftime import Datetime360Day

data=xr.open_mfdataset(os.path.join(input_folder,"*_pa*.nc"),
                       concat_dim="time",parallel=True).surface_temperature
lat,lon=my.DataArray(data).get_spatial_coords()                       
data = data.rename({lon:'longitude',lat:'latitude'})

land_mask=xr.open_dataarray(my.UM.land_mask_file())
time=[Datetime360Day(0,m,16,0) for m in np.arange(1,13)]
ref=xr.open_dataarray("/g/data/w40/dm5220/ancil/ref/qrclim.sst_noland.nc").squeeze()

annual_cycle = data.isel(time=slice(-30*12,None)).groupby("time.month").mean('time',keep_attrs=True)
annual_cycle = annual_cycle.rename({'month':'t'}).assign_coords(t=time)

ts=ref.where(land_mask==1,annual_cycle).astype(np.float32)
ts.attrs['units'] = 'K' ; ts.attrs['long_name'] = 'Surface Temperature' ; ts.name= 'surface_temperature'
del ts['forecast_reference_time'];del ts['surface'];del ts['height']

encoding = {ts.name: {'zlib':True,'shuffle':True,'complevel':4}}
with ProgressBar():
    ts.to_netcdf(output_file,encoding=encoding)
