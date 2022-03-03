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

vals = {"p":0.015,"m":-0.015}
levs = {"Lower atmosphere":[1,7],
        "Mid atmosphere":[7,13],
        "High atmosphere":[13,19],
        "Top atmosphere":[19,25]}
levs_save={"Lower atmosphere":"la",
        "Mid atmosphere":"ma",
        "High atmosphere":"ha",
        "Top atmosphere":"ta"}
lats = {"Equatorial":[-10,10],
        "Extratropics":[-90,-35,35,90],
        "Global":[-90,90]}
lats_save = {"Equatorial":'equa',
        "Extratropics":'extr',
        "Global":'global'}

base_dir = sys.argv[1]
file_output_folder = os.path.join(base_dir,"files_for_xancil")
os.makedirs(file_output_folder,exist_ok=True)
figure_output_folder = os.path.join(base_dir,"figures")
os.makedirs(figure_output_folder,exist_ok=True)
cmaps = {"p":colors.ListedColormap(['white','red']),
         "m":colors.ListedColormap(['blue','white'])}

name = "mlev_ancil"
data=dask.array.from_array(np.zeros([360,38,73,96]),name=name)
da=my.DataArray(data,
    dims=('time', 'model_level_number', 'latitude', 'longitude'),
    coords=[np.arange(1,361),np.arange(1,39),my.UM.latitude,my.UM.longitude])

for val_id,val in vals.items():
    for atm,lev in levs.items():
        for arealat,lat in lats.items():
            if arealat == "Global":
                newval=val*0.008/0.015
            else:
                newval=val
            # Condition for latitude
            clat0=np.logical_and(da.latitude>=lat[0],da.latitude<=lat[1])
            if len(lat) > 2:
                clat=np.logical_or(clat0,np.logical_and(da.latitude>=lat[2],da.latitude<=lat[3]))
            else:
                clat=clat0
            # Condition for model levels
            clev=np.logical_and(da.model_level_number>=lev[0],da.model_level_number<=lev[1])
            cond = np.logical_and(clat,clev)
            # # Condition for longitude
            # clon0=np.logical_and(da.longitude>=lon[0],da.longitude<=lon[1])
            # if len(lon) > 2:
            #     clon=np.logical_or(clon0,np.logical_and(da.longitude>=lon[2],da.longitude<=lon[3])):
            # else:
            #     clon=clon0
            # cond = np.logical_and(cond,np.logical_not(clon))
            cond=np.logical_not(cond)
            
            new=my.DataArray(da.where(cond,newval))
            outname=f"{val_id}_{lats_save[arealat]}_{levs_save[atm]}"
            new.to_netcdf(os.path.join(file_output_folder,f"{outname}.nc"))
            # Plot lat-lon            
            plt.figure()
            new.annual_mean().sel(model_level_number=lev[0]).plotvar(
                projection=False,
                cmap=cmaps[val_id],
                levels=2,
                statistics=False,
                units='K/(30min)',
                grid=True,
                title=f"{newval} {arealat} {atm}",
                outpath=os.path.join(figure_output_folder,f"lat-lon_{outname}"),
                )   
            plt.clf()
            # Plot lev-lon                
            new.annual_mean().sel(latitude=lat[0],method='backfill').plotlev(
                cmap=cmaps[val_id],
                levels=2,
                units='K/(30min)',
                double_axis=True,
                outpath=os.path.join(figure_output_folder,f"lev-lon_{outname}"),
                title=f"{newval} {arealat} {atm}",
                )
            plt.clf()
            # Plot lev-lat                
            new.annual_mean().sel(longitude=0).plotlev(
                cmap=cmaps[val_id],
                levels=2,
                units='K/(30min)',
                double_axis=True,
                outpath=os.path.join(figure_output_folder,f"lev-lat_{outname}"),
                title=f"{newval} {arealat} {atm}",
                )
            plt.clf()