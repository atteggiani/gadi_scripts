import myfuncs as my
import xarray as xr
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
import concurrent.futures
import dask
from dask.diagnostics import ProgressBar
from decorators import timer
from metpy.interpolate import log_interpolate_1d
from metpy.units import units
from scipy.interpolate import interp1d
import matplotlib.colors as colors

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
        
outpath = "/g/data3/w48/dm5220/data/figures"
input_folder = "/g/data/w48/dm5220/data"

nlevs=30
d=read_data(input_folder,["ctl"])[0]
data=d.air_temperature_0.isel(model_level_number=slice(0,nlevs))
p0=d.surface_air_pressure
slevs=d.sigma.isel(model_level_number=slice(0,nlevs))
slevs[-1]=1e-300 #avoid nan because of log(0)
pressure=((p0*slevs)).values.transpose(0,3,1,2)*units.Pa
plevs=np.flip(d.pressure).values*units.hPa

a=log_interpolate_1d(plevs, pressure, data.values, axis=1)
new=np.flip(a,axis=1)
daskarr=dask.array.from_array(new,chunks=[12,16,73,96],name=data.name + "_plev")
x=xr.DataArray(data=daskarr,
        coords=(data.time,
                d.pressure,
                data.latitude,
                data.longitude),
        dims=("time","pressure","latitude","longitude"),
        attrs={"standard_name":data.name + "_plev",
               "Converted": "Converted from 'model_level_number' vertical coordinates using metpy's 'log_interpolate_1d' function.",
               "units":"K",
               "grid_mapping":"latitude_longitude"})

y=d.air_temperature

plt.figure()
my.DataArray(x).annual_mean().mean("longitude").plotlev(levels=np.linspace(200,300,50))
plt.figure()
my.DataArray(y).annual_mean().mean("longitude_0").plotlev(levels=np.linspace(200,300,50))

x1=x.interp(longitude=y.longitude_0,latitude=y.latitude_0)

plt.figure()
my.DataArray(x1-y).annual_mean().mean("longitude_0").plotlev(levels=np.linspace(-5,30,50),norm=colors.TwoSlopeNorm(vmin=-5,vcenter=
0,vmax=30))

# newd=d.assign({data.name + "_plev":x})