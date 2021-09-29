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
            data.append(xr.open_mfdataset(
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

d=read_data(input_folder,["ctl"])[0]
tair_pr=d.air_temperature

nlevs=29
tair_lev=d.air_temperature_0.isel(model_level_number=slice(0,nlevs))
p0=d.surface_air_pressure
slevs=d.sigma.isel(model_level_number=slice(0,nlevs))
slevs=slevs.where(slevs!=0,1e-300) #avoid nan because of log(0)
pressure=((p0*slevs)).values.transpose(0,3,1,2)*units.Pa
plevs=np.flip(d.pressure).values*units.hPa


a=log_interpolate_1d(plevs, pressure, tair_lev.values, axis=1)
new=np.flip(a,axis=1)
daskarr=dask.array.from_array(new,chunks=[12,16,73,96],name=tair_lev.name + "_plev")
tair_conv=xr.DataArray(data=daskarr,
        coords=(tair_lev.time,
                d.pressure,
                tair_lev.latitude,
                tair_lev.longitude),
        dims=("time","pressure","latitude","longitude"),
        attrs={"standard_name":tair_lev.name + "_plev",
               "Converted": "Converted from 'model_level_number' vertical coordinates using metpy's 'log_interpolate_1d' function.",
               "units":"K",
               "grid_mapping":"latitude_longitude"})

plt.figure()
tair_conv.mean(["time","longitude"]).plot(
        levels=np.linspace(200,300,50),
        yincrease=False,
        yscale='log')   
ax=plt.gca()             
ax.set_xticks(np.arange(-90,90+30,30))
ax.set_xticklabels(["90S","60S","30S","0","30N","60N","90N"])        
ax.set_ylim([1000,50])
ax.set_yticks([1000,800,600,400,200,50])
ax.set_yticklabels(["1000","800","600","400","200","50"])
plt.title("Tair_conv")
# plt.savefig("Tair_conv.png",dpi=300)

plt.figure()
tair_pr.mean(["time","longitude_0"]).plot(
        levels=np.linspace(200,300,50),
        yincrease=False,
        yscale='log')   
ax=plt.gca()             
ax.set_xticks(np.arange(-90,90+30,30))
ax.set_xticklabels(["90S","60S","30S","0","30N","60N","90N"])        
ax.set_ylim([1000,50])
ax.set_yticks([1000,800,600,400,200,50])
ax.set_yticklabels(["1000","800","600","400","200","50"])
plt.title("Tair_pr")
# plt.savefig("Tair_pr.png",dpi=300)

tair_conv_interp=tair_conv.interp(longitude=tair_pr.longitude_0,latitude=tair_pr.latitude_0)

plt.figure()
(tair_conv_interp-tair_pr).mean(["time","longitude_0"]).plot(
        levels=np.linspace(-10,30,50),
        norm=colors.TwoSlopeNorm(0,-10,30),
        yincrease=False,
        yscale='log')   
ax=plt.gca()             
ax.set_xticks(np.arange(-90,90+30,30))
ax.set_xticklabels(["90S","60S","30S","0","30N","60N","90N"])        
ax.set_ylim([1000,50])
ax.set_yticks([1000,800,600,400,200,50])
ax.set_yticklabels(["1000","800","600","400","200","50"])
plt.title("Difference")
# plt.savefig("Difference.png",dpi=300)


# newd=d.assign({data.name + "_plev":x})