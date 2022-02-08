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
from matplotlib.patches import Rectangle

def rectangle(dim1,dim2):
    patches=[]
    ndim1=[]
    if len(dim1) > 2:
        dim1=[dim1[0],dim1[2]]
    for d in dim1:
        if d > 180:
            ndim1.append(d-360)
        else:
            ndim1.append(d)
    if ndim1[0] < ndim1[1]:
        patches.append(
            Rectangle((ndim1[0],dim2[0]),
                       ndim1[1]-ndim1[0],
                       dim2[1]-dim2[0],
                       fill=False,
                       ls='--',
                       color='red'))
    else:
        patches.append(
            Rectangle((ndim1[0],dim2[0]),
                       180-ndim1[0],
                       dim2[1]-dim2[0],
                       fill=False,
                       ls='--',
                       color='red'))
        patches.append(
            Rectangle((-180,dim2[0]),
                       180+ndim1[1],
                       dim2[1]-dim2[0],
                       fill=False,
                       ls='--',
                       color='red'))
    return patches

mlev = {"la":[1,7],
        "ma":[7,13],
        "ha":[13,19],
        "ta":[19,25]}
plev = {"la":[1000,890],
        "ma":[870,630],
        "ha":[630,400],
        "ta":[400,200]}
lat = [-20,20]
lon = {"pac":[165,255],
        "ama":[255,345],
        "atl":[288.75,356.25,18.75],
        "afr":[341.25,356.25,71.25],
        "ind":[33.75,123.75]}

def sel_lon(x):
    if len(lon[area]) == 2:
        return x.sel(longitude=slice(*lon[area])).longitude_mean()
    else:
        cond=np.where(np.logical_or(np.logical_and(d.longitude>=lon[area][0],d.longitude<=lon[area][1]),d.longitude<=lon[area][2]))[0]
        return x.isel(longitude=cond).longitude_mean()
sel_lat=lambda x: x.sel(latitude=slice(*lat)).latitude_mean()

out_folder='/g/data/w48/dm5220/data/figures/tac_rad_test'
nyears=20
ctl=my.UM.read_data('4co2_sw_x0.9452_offset')
files=['p_ind_la',]
for file in files:
    d=my.UM.read_data(f'4co2_sw-_{file}')
    # d=my.Dataset(d.to_pressure_lev()) #TO DELETE
    change,area,atm=file.split('_')
    anom=lambda var: d[var]-ctl[var]
    p=lambda var: d[var].t_student_probability(ctl[var],num_years=nyears)

    def plot_level(var,levs,mean,func=lambda x: x*1,**kwargs):
        if mean == 'lonmean':
            selection=sel_lon
            core_dim=lat
        else:
            selection=sel_lat
            core_dim=lon[area]
        if 'outpath' in kwargs:
            outpath=kwargs.pop('outpath')
            save=True
        else:
            save=False
        rec=rectangle(core_dim,levs[atm])
        P=p(var)
        data=anom(var).annual_mean(12*nyears)
        data=selection(data)
        data=func(data)
        data.plotlev(
            t_student=selection(P),
            double_axis=True,
            **kwargs)
        for r in rec:
            plt.gca().add_patch(r)
        if save:
            plt.savefig(outpath, dpi=300, bbox_inches='tight')

    def plot(var,func=lambda x: x*1,**kwargs):
        rec=rectangle(lon[area],lat)
        if 'outpath' in kwargs:
            outpath=kwargs.pop('outpath')
            save=True
        else:
            save=False
        P=p(var)
        data=anom(var).annual_mean(12*nyears)
        data=func(data)
        data.plotvar(
            t_student=P,
            **kwargs)
        for r in rec:
            plt.gca().add_patch(r)
        if save:
            plt.savefig(outpath, dpi=300, bbox_inches='tight')

    def plot_profile(var,levs,func=lambda x: x*1,**kwargs):
        if 'outpath' in kwargs:
            outpath=kwargs.pop('outpath')
            save=True
        else:
            save=False
        data=anom(var)
        data=sel_lat(sel_lon(data))
        data=func(data)
        data.plotprof(
            timesteps=12*nyears,
            double_axis=True,
            **kwargs)
        xlim=plt.gca().get_xlim()
        plt.hlines(levs[atm][0],*xlim,color='red',lw=1,ls='--')
        plt.hlines(levs[atm][1],*xlim,color='red',lw=1,ls='--')
        if save:
            plt.savefig(outpath, dpi=300, bbox_inches='tight')


    # TSURF 
    var='surface_temperature'
    plt.figure()
    plot(var,
        levels=np.linspace(-2,2,20),
        du=0.5,
        units='K',
        cmap=my.Colormaps.div_tsurf,
        title=f'Surface Temperature | {file}',
        outpath=os.path.join(out_folder,f'{file}_tsurf'))
    plt.clf()
    # PRECIP
    var='precipitation_flux'
    plot(var,
        func=lambda x: x.to_mm_per_day(),
        levels=np.linspace(-2,2,20),
        du=0.5,
        units='mm/day',
        cmap=my.Colormaps.div_precip,
        title=f'Precipitation | {file}',
        outpath=os.path.join(out_folder,f'{file}_precip'))
    plt.clf()

    # TAIR 
    # plev (lonmean)
    var='air_temperature_0_plev'
    plot_level(var,plev,'lonmean',
        levels=np.linspace(-2,2,20),
        du=0.5,
        units='K',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {file}',
        outpath=os.path.join(out_folder,f'{file}_tair_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,plev,'latmean',
        levels=np.linspace(-2,2,20),
        du=0.5,
        units='K',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {file}',
        outpath=os.path.join(out_folder,f'{file}_tair_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='air_temperature_0'
    plot_level(var,mlev,'lonmean',
        levels=np.linspace(-2,2,20),
        du=0.5,
        units='K',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {file}',
        outpath=os.path.join(out_folder,f'{file}_tair_lonmean_mlev'))
    plt.clf()
    # mlev (latmean)
    plot_level(var,mlev,'latmean',
        levels=np.linspace(-2,2,20),
        du=0.5,
        units='K',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {file}',
        outpath=os.path.join(out_folder,f'{file}_tair_latmean_mlev'))
    plt.clf()

    # LW HEATIING RATES
    # plev (lonmean)
    var='tendency_of_air_temperature_due_to_longwave_heating_plev'
    plot_level(var,plev,'lonmean',func=lambda x: x.to_K_per_day(),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_LWhrate_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,plev,'latmean',func=lambda x: x.to_K_per_day(),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_LWhrate_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='tendency_of_air_temperature_due_to_longwave_heating'
    plot_level(var,mlev,'lonmean',func=lambda x: x.to_K_per_day(force=True),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_LWhrate_lonmean_mlev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,mlev,'latmean',func=lambda x: x.to_K_per_day(force=True),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_LWhrate_latmean_mlev'))
    plt.clf()

    # SW HEATIING RATES
    # plev (lonmean)
    var='tendency_of_air_temperature_due_to_shortwave_heating_plev'
    plot_level(var,plev,'lonmean',func=lambda x: x.to_K_per_day(),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_SWhrate_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,plev,'latmean',func=lambda x: x.to_K_per_day(),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_SWhrate_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='tendency_of_air_temperature_due_to_shortwave_heating'
    plot_level(var,mlev,'lonmean',func=lambda x: x.to_K_per_day(force=True),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_SWhrate_lonmean_mlev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,mlev,'latmean',func=lambda x: x.to_K_per_day(force=True),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_SWhrate_latmean_mlev'))
    plt.clf()

    # TOT HEATIING RATES
    # plev (lonmean)
    var='tendency_of_air_temperature_due_to_total_heating_plev'
    plot_level(var,plev,'lonmean',func=lambda x: x.to_K_per_day(),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_TOThrate_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,plev,'latmean',func=lambda x: x.to_K_per_day(),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_TOThrate_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='tendency_of_air_temperature_due_to_total_heating'
    plot_level(var,mlev,'lonmean',func=lambda x: x.to_K_per_day(force=True),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_TOThrate_lonmean_mlev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,mlev,'latmean',func=lambda x: x.to_K_per_day(force=True),
        levels=np.linspace(-0.1,0.1,20),
        du=0.02,
        units='K/day',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {file}',
        outpath=os.path.join(out_folder,f'{file}_TOThrate_latmean_mlev'))
    plt.clf()

    # TAIR VERTICAL PROFILE
    # plev
    var='air_temperature_0_plev'
    plot_profile(var,plev,
                xlim=[-5,3],
                dx=1,
                units='K',
                title=f'Air Temperature | {file}',
                outpath=os.path.join(out_folder,f'{file}_tair_vertprof_plev'))
    plt.clf()
    # mlev
    var='air_temperature_0'
    plot_profile(var,mlev,
                xlim=[-5,3],
                dx=1,
                units='K',
                title=f'Air Temperature | {file}',
                outpath=os.path.join(out_folder,f'{file}_tair_vertprof_mlev'))
    plt.clf()

    # TOT HRATE VERTICAL PROFILE
    # plev
    var='tendency_of_air_temperature_due_to_total_heating_plev'
    plot_profile(var,plev,
                func=lambda x: x.to_K_per_day(force=True),
                xlim=[-0.4,0.4],
                dx=0.1,
                units='K/day',
                title=f'TOT Heating Rate | {file}',
                outpath=os.path.join(out_folder,f'{file}_TOThrate_vertprof_plev'))
    plt.clf()
    # mlev
    var='tendency_of_air_temperature_due_to_total_heating'
    plot_profile(var,mlev,
                func=lambda x: x.to_K_per_day(force=True),
                xlim=[-0.4,0.4],
                dx=0.1,
                units='K/day',
                title=f'TOT Heating Rate | {file}',
                outpath=os.path.join(out_folder,f'{file}_TOThrate_vertprof_mlev'))
    plt.clf()
