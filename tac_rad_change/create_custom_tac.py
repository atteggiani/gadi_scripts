import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os
import sys
import dask
import cartopy.crs as ccrs
import matplotlib.colors as colors
import matplotlib.cm as cmap
import matplotlib.pyplot as plt

# vals = {"p":0.015,"m":-0.015}
# lat = [-20,20]
# lons = {"Pacific":[165,255],
#         "Amazon":[255,345],
#         "Atlantic":[288.75,356.25,18.75],
#         "Africa":[341.25,356.25,71.25],
#         "Indian":[33.75,123.75]}

change = [
    {'val':-0.015,'lat':[[-55,-30]],'lon':[[0,360]],'lev':[7,13]}, 
    {'val': 0.015,'lat':[[-90,-60]],'lon':[[0,360]],'lev':[7,13],},
    {'val':-0.013,'lat':[[35,80]],'lon':[[0,360]],'lev':[7,13]},
    {'val':-0.015,'lat':[[-20,20]],'lon':[[310,360],[0,40]],'lev':[7,13]},
]

outname = sys.argv[1]


base_dir = '/g/data3/w40/dm5220/ancil/user_mlevel/tac_rad_change'
file_output_folder = os.path.join(base_dir,"files_for_xancil")
logfile = os.path.join(file_output_folder,f'logfile_{outname}')
os.makedirs(file_output_folder,exist_ok=True)
figure_output_folder = os.path.join(base_dir,"figures")
os.makedirs(figure_output_folder,exist_ok=True)

name = "mlev_ancil"
data=dask.array.from_array(np.zeros([360,38,73,96]),name=name)
da=my.DataArray(data,
    dims=('time', 'model_level_number', 'latitude', 'longitude'),
    coords=[np.arange(1,361),np.arange(1,39),my.UM.latitude,my.UM.longitude])

# Create new dataarray based on change
cond=False
for ch in change:
    # Condition for latitude
    clat=False
    clon=False
    for lat in ch['lat']:
        clat=np.logical_or(clat,np.logical_and(da.latitude>=lat[0],da.latitude<=lat[1]))
    # Condition for longitude
    for lon in ch['lon']:
        clon=np.logical_or(clon,np.logical_and(da.longitude>=lon[0],da.longitude<=lon[1]))
    ctot = np.logical_and(clat,clon)
    # Condition for model levels
    lev=ch['lev']
    clev=np.logical_and(da.model_level_number>=lev[0],da.model_level_number<=lev[1])
    ctot = np.logical_and(ctot,clev)
    cond=np.logical_or(ctot,cond)
    
notcond=np.logical_not(cond)    
new=my.DataArray(da.where(notcond,ch['val']))
# Write dataarray
out=os.path.join(file_output_folder,f"{outname}.nc")
new.to_netcdf(os.path.join(file_output_folder,f"{outname}.nc"))

# Write logfile to keep track of changes
with open(logfile,'w') as f:
    f.write('='*15 + '\n')
    f.write(f'FILE: {out}\n')
    for i,ch in enumerate(change):
        f.write(' '*4 + f"val:{ch['val']} | lat:{ch['lat']} | lon:{ch['lon']} | lev:{ch['lev']}\n")
    f.write('='*15 + '\n'*2)

# # # PLOT 3D
# def pp():
#     x = new.latitude
#     y = new.longitude
#     z = new.model_level_number.sel(model_level_number=slice(1,22))

#     A,B,C = np.meshgrid(x, y, z)

#     # Your 4dimension, only for example use yours
#     K = np.transpose(new.isel(time=0).sel(model_level_number=slice(1,22)).values,(2,1,0))
#     K_mask=np.ma.masked_where(K == 0)
#     # K = np.where(K==0,np.nan,K)
#     # Creating figure
#     fig = plt.figure()
#     ax = plt.axes(projection="3d")

#     # Creating plot
#     img=ax.scatter3D(A,B,C, c=K, alpha=0.6, marker='.',cmap=cmap.jet)
#     plt.colorbar(img)
#     plt.show()
#     print(K.shape)
# pp()