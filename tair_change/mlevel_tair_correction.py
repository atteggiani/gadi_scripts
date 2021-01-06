#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-20.10/bin/python3

import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
import os
import numpy as np

## PARSE ARGUMENTS
parser=ArgumentParser()
# parser.add_argument('-i','--input',type=str)
parser.add_argument('-o','--output',type=str)
parser.add_argument('-c','--change',type=np.float)
# parser.add_argument('--id','--exp_id',type=str)
args=parser.parse_args()

# input_folder=args.input
out_file=args.output
change=args.change

import myfuncs as my
import xarray as xr
from importlib import reload
from cftime import Datetime360Day as dt360

#Create base xarray with all values equal 0
time = [dt360(0,m,16) for m in range(1,13)]
lat = my.Constants.um.latitude
lon = my.Constants.um.longitude 
levs = my.Constants.um.hybrid_height
coords=(time,levs,lat,lon)
b=np.zeros([len(x) for x in coords],dtype=np.float32)
tac=xr.DataArray(data=b, dims=("time","hybrid_ht","latitude","longitude") ,coords=coords,name="tair_corrections")
tac+=change

output_file = "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/files_for_xancil/{}.nc".format(out_file)
encoding = {tac.name: {'zlib':True,'shuffle':True,'complevel':4,'chunksizes': [1,8,73,96]}}
tac.to_netcdf(output_file,encoding=encoding)

