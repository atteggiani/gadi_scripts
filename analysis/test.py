import myfuncs as my
import xarray as xr
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
import concurrent.futures
import dask
from dask.diagnostics import ProgressBar
from decorators import timed
from metpy.interpolate import log_interpolate_1d
from metpy.units import units
from scipy.interpolate import interp1d
import matplotlib.colors as colors
from importlib import reload

def read_data(input_folder,files):
        data=[]
        for file in files:
            data.append(my.open_mfdataset(
                os.path.join(
                        input_folder,
                        f"{file}/*_pa*.nc"),
                parallel=True,
                combine="nested",
                concat_dim="time",
                compat='override',
                coords='minimal',
                ))
        return data

input_folder = "/g/data/w48/dm5220/data"
d=read_data(input_folder,["ctl"])[0]
# data=d.air_temperature_0

def to_pressure_lev(x,data_vars=None):
    if 'air_pressure' not in x:
        return
    if data_vars is None:
        data_vars=['combined_cloud_amount',
                   'air_temperature_0',
                   'large_scale_rainfall_flux',
                   'tendency_of_air_temperature_due_to_longwave_heating',
                   'tendency_of_air_temperature_due_to_longwave_heating_assuming_clear_sky',
                   'tendency_of_air_temperature_due_to_shortwave_heating',
                   'tendency_of_air_temperature_due_to_shortwave_heating_assuming_clear_sky',
                   ]
    plevs = [1000, 925, 850, 700,
             600, 500, 400, 300,
             250, 200, 150, 100,
             70, 50, 30, 20] * units.hPa
    pr = (x['air_pressure']).values * units.Pa
    for var in data_vars:
        if var not in x: continue
        data = x[var]        
        new=np.flip(
            log_interpolate_1d(plevs, pr, data.values, axis=1),
            axis=1)
        new_name=data.name + "_plev"
        
        converted=xr.DataArray(data=dask.array.from_array(new,name=new_name),
            coords=(data.time,
                    d.pressure,
                    data.latitude,
                    data.longitude),
            dims=("time","pressure","latitude","longitude"),
            attrs={"standard_name":new_name,
                "units":"K",
                "grid_mapping":"latitude_longitude",
                "Converted":"Converted from 'model_level_number' vertical coordinates using metpy's 'log_interpolate_1d' function."})
        x=x.assign({new_name:converted})
    return x

# pr = (d['air_pressure']).values*units.Pa
# a=log_interpolate_1d(plevs, pr, data.values, axis=1)
# new=np.flip(a,axis=1)

converted=to_pressure_lev(d)

converted.to_netcdf(path="/g/data3/w48/dm5220/scripts/analysis/data.nc",
            mode='w')
# x.to_netcdf(path="/g/data3/w48/dm5220/scripts/analysis/data.nc",
#             mode='a')            