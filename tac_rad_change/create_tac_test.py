import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os
import sys
import dask
import cartopy.crs as ccrs
import matplotlib.colors as colors
import matplotlib.pyplot as plt

vals = {"p":0.02,
        "m":-0.02}
levs = {"Lower atmosphere":[1,7],
        "Mid atmosphere":[7,13],
        "High atmosphere":[13,19],
        "Top atmosphere":[19,25]}
plevs=[1000,870,630,400,200]        
levs_save={"Lower atmosphere":"la",
        "Mid atmosphere":"ma",
        "High atmosphere":"ha",
        "Top atmosphere":"ta"}
lat = [-20,20]
lons = {"Pacific":[165,255],
        "Amazon":[255,345],
        "Atlantic":[288.75,356.25,18.75],
        "Africa":[341.25,356.25,71.25],
        "Indian":[33.75,123.75]}
base_dir = sys.argv[1]
file_output_folder = os.path.join(base_dir,"files_for_xancil")
os.makedirs(file_output_folder,exist_ok=True)
figure_output_folder = os.path.join(base_dir,"figures")
os.makedirs(figure_output_folder,exist_ok=True)
name = "mlev_ancil"
cmaps = {"p":colors.ListedColormap(['white','red']),
         "m":colors.ListedColormap(['blue','white'])}

data=dask.array.from_array(np.zeros([360,38,73,96]),name=name)
da=my.DataArray(data,
    dims=('time', 'model_level_number', 'latitude', 'longitude'),
    coords=[np.arange(1,361),np.arange(1,39),my.UM.latitude,my.UM.longitude])

for val_id,val in vals.items():
    for atm,lev in levs.items():
        for area,lon in lons.items():
            # Condition for latitude
            c0=np.logical_and(da.latitude>=lat[0],da.latitude<=lat[1])
            # Condition for model levels
            c1=np.logical_and(da.model_level_number>=lev[0],da.model_level_number<=lev[1])
            # Condition for longitude
            c2=np.logical_and(da.longitude>=lon[0],da.longitude<=lon[1])
            if len(lon) == 3:
                c2=np.logical_or(c2,np.logical_and(da.longitude>=0,da.longitude<=lon[2]))
            # Join conditions
            cond = np.logical_not(np.logical_and(np.logical_and(c0,c1),c2))
            new=my.DataArray(da.where(cond,val))
            outname=f"{val_id}_{area.lower()[:3]}_{levs_save[atm]}"
            new.to_netcdf(os.path.join(file_output_folder,f"{outname}.nc"))
            # Plot lat-lon            
            plt.figure()
            new.annual_mean().isel(model_level_number=lev[0]).plotvar(
                projection=False,
                cmap=cmaps[val_id],
                levels=2,
                statistics=False,
                units='K/(30min)',
                grid=True,
                title=f"{val} {area} {atm}",
                outpath=os.path.join(figure_output_folder,f"lat-lon_{outname}"),
                )   
            plt.clf()
            # Plot lev-lon                
            new.annual_mean().sel(latitude=lat[0]).plotlev(
                cmap=cmaps[val_id],
                levels=2,
                units='K/(30min)',
                double_axis=True,
                outpath=os.path.join(figure_output_folder,f"lev-lon_{outname}"),
                title=f"{val} {area} {atm}",
                )
            plt.clf()
            # Plot lev-lat                
            new.annual_mean().sel(longitude=lon[0]).plotlev(
                cmap=cmaps[val_id],
                levels=2,
                units='K/(30min)',
                double_axis=True,
                outpath=os.path.join(figure_output_folder,f"lev-lat_{outname}"),
                title=f"{val} {area} {atm}",
                )
            plt.clf()
