import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os
import sys
import dask
import cartopy.crs as ccrs
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

# vals = {"p":0.015,"m":-0.015}
# lat = [-20,20]
# lons = {"Pacific":[165,255],
#         "Amazon":[255,345],
#         "Atlantic":[288.75,356.25,18.75],
#         "Africa":[341.25,356.25,71.25],
#         "Indian":[33.75,123.75]}

change = [
    {'val':-0.009,'lat':[[-20,20]],'lon':[[310,360],[0,40]],'lev':[7,13]},
    {'val':-0.001,'lat':[[-55,-30]],'lon':[[0,360]],'lev':[7,13]}, 
    # {'val': 0.015,'lat':[[-90,-60]],'lon':[[0,360]],'lev':[7,13],},
    # {'val':-0.013,'lat':[[35,80]],'lon':[[0,360]],'lev':[7,13]},
]
(latl,lonl,levl)=(0,0,9)

# # PLOT 3D
def pp(data,lat=0,lon=0,lev=9):
    x = new.latitude
    y = new.longitude
    z = new.model_level_number.sel(model_level_number=slice(1,22))

    A,B,C = np.meshgrid(x, y, z)

    # Your 4dimension, only for example use yours
    K = np.transpose(data.isel(time=0).sel(model_level_number=slice(1,22)).values,(2,1,0))
    K = np.where(K==0,np.nan,K)
    # cmap=my.Colormaps.div_precip.copy().set_bad([0,0,0,0])
    colorArray=[[0,0,1,0.3],[0,1,1,0.3],[0,1,0,0.3],[1,1,0,0.3],[1,0,0,0.3]]
    cmap=colors.LinearSegmentedColormap.from_list('mycmap',colors=colorArray,N=256)
    cmap.set_bad([0,0,0,0])
    # Creating plot
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection="3d")
    ax.view_init(35,70)
    img=ax.scatter3D(A,B,C, c=K, marker='.',cmap=cmap,
        norm=colors.TwoSlopeNorm(vmin=-0.02,vmax=0.02,vcenter=0))
    plt.colorbar(img)
    # xaxis
    ax.set_xlim(-90,90)
    ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    # yaxis
    ax.set_ylim(0,360)
    ax.yaxis.set_major_locator(MultipleLocator(60))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_minor_locator(MultipleLocator(30))
    # zaxis
    ax.set_zlim(0,21)
    ax.zaxis.set_major_locator(MultipleLocator(7))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.zaxis.set_minor_locator(MultipleLocator(1))

    # Plot lev line 
    x1 = (lat,lat)
    y1 = (lon,lon)
    z1 = ax.get_zlim()
    ax.plot(x1,y1,z1,ls='--',alpha=0.8, lw=1,color='black')
    # Plot lon line 
    x1 = (lat,lat)
    y1 = ax.get_ylim()
    z1 = (lev,lev)
    ax.plot(x1,y1,z1,ls='--',alpha=0.8, lw=1,color='black')
    # Plot lat line 
    x1 = ax.get_xlim()
    y1 = (lon,lon)
    z1 = (lev,lev)
    ax.plot(x1,y1,z1,ls='--',alpha=0.8, lw=1,color='black')
    # plt.show()
    plt.savefig(os.path.join(figure_output_folder,f"{outname}_flux3d"),
        bbox_inches='tight',dpi=300)
# PLOT LEV
def plev(x,lat=0,lon=0):
    x=x.sel(model_level_number=slice(0,21))
    s=x.sel(latitude=lat,longitude=lon)[0]
    plt.figure()
    s.plot(y='model_level_number')
    plt.ylim([0,21])
    plt.xlim([-0.02,0.02])
    ax=plt.gca()
    ax.yaxis.set_major_locator(MultipleLocator(7))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    plt.title(f'Model Level Number profile (lat={lat} ; lon={lon})')
    plt.grid(which='both')
    # plt.show()
    plt.savefig(os.path.join(figure_output_folder,f"{outname}_levprof"),
        bbox_inches='tight',dpi=300)
# PLOT LON
def plon(x,lat=0,lev=9):
    s=x.sel(latitude=lat,model_level_number=lev)[0]
    plt.figure()
    s.plot()
    plt.xlim([0,360])
    plt.ylim([-0.02,0.02])
    ax=plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(60))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    plt.title(f'Longitude profile (lat={lat} ; lev={lev})')
    plt.grid(which='both')
    # plt.show()
    plt.savefig(os.path.join(figure_output_folder,f"{outname}_lonprof"),
        bbox_inches='tight',dpi=300)
# PLOT LAT
def plat(x,lon=0,lev=9):
    s=x.sel(longitude=lon,model_level_number=lev)[0]
    plt.figure()
    s.plot()
    plt.xlim([-90,90])
    plt.ylim([-0.02,0.02])
    ax=plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    plt.title(f'Latitude profile (lon={lon} ; lev={lev})')
    plt.grid(which='both')
    # plt.show()
    plt.savefig(os.path.join(figure_output_folder,f"{outname}_latprof"),
        bbox_inches='tight',dpi=300)
   
outname = sys.argv[1]

base_dir = '/g/data3/w40/dm5220/ancil/user_mlevel/tac_rad_change'
file_output_folder = os.path.join(base_dir,"files_for_xancil")
logfile = os.path.join(file_output_folder,f'logfile_{outname}')
os.makedirs(file_output_folder,exist_ok=True)
figure_output_folder = os.path.join(base_dir,"figures/custom")
os.makedirs(figure_output_folder,exist_ok=True)

name = "mlev_ancil"
data=dask.array.from_array(np.zeros([360,38,73,96]),name=name)
da=my.DataArray(data,
    dims=('time', 'model_level_number', 'latitude', 'longitude'),
    coords=[np.arange(1,361),np.arange(1,39),my.UM.latitude,my.UM.longitude])

# Create new dataarray based on change
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
    cond = np.logical_and(ctot,clev)
    notcond=np.logical_not(cond)    
    da=my.DataArray(da.where(notcond,ch['val']))

# Apply filter
# LEV
func=lambda x: savgol_filter(x,
    window_length=3,
    polyorder = 1,
    axis = da.dims.index('model_level_number'),
    mode='nearest')
new=xr.apply_ufunc(func,da,dask='parallelized')
new=xr.apply_ufunc(func,new,dask='parallelized')
# LON
func=lambda x: savgol_filter(x,
    window_length=5,
    polyorder = 1,
    axis = new.dims.index('longitude'),
    mode='nearest')
new=xr.apply_ufunc(func,new,dask='parallelized')
new=xr.apply_ufunc(func,new,dask='parallelized')
# LAT
func=lambda x: savgol_filter(x,
    window_length=3,
    polyorder = 1,
    axis = new.dims.index('latitude'),
    mode='nearest')
new=xr.apply_ufunc(func,new,dask='parallelized')
new=xr.apply_ufunc(func,new,dask='parallelized')

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
 
# PLOT
pp(new,lat=latl,lon=lonl,lev=levl)
plev(new,lat=latl,lon=lonl)
plon(new,lat=latl,lev=levl)
plat(new,lon=lonl,lev=levl)