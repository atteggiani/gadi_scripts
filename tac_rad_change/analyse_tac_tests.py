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

def sel_lon(x):
    if len(lon[area]) == 2:
        return x.sel(longitude=slice(*lon[area])).longitude_mean()
    else:
        cond=np.where(np.logical_or(np.logical_and(d.longitude>=lon[area][0],d.longitude<=lon[area][1]),d.longitude<=lon[area][2]))[0]
        return x.isel(longitude=cond).longitude_mean()

def sel_lat(x):
    if len(lat[area]) == 2:
        return x.sel(latitude=slice(*lat[area])).latitude_mean()
    else:
        cond=np.logical_or(np.logical_and(d.latitude>=lat[area][0],d.latitude<=lat[area][1]),
                           np.logical_and(d.latitude>=lat[area][2],d.latitude<=lat[area][3]))
        return x.isel(latitude=cond).latitude_mean()

def rectangle(lat=None,lon=None,lev=None):
    patches=[]
    X=[]
    Y=[]
    
    if lev is None or lat is None:
        if len(lon) > 2:
            lon=[lon[0],lon[2]]
        lon=[l-360 if l >= 180 else l for l in lon]
        if lon[0] < 0:
            lon.sort()
            X.append([lon[0],lon[1]-lon[0]])
        else:
            if lon[1] > 0:
                X.append([lon[0],lon[1]-lon[0]])
            else:
                X.append([lon[0],180-lon[0]])
                X.append([-180,180+lon[1]])
    else:
        X.append([lat[0],lat[1]-lat[0]])
        if len(lat) > 2:
            X.append([lat[2],lat[3]-lat[2]])

    if lev is not None:
        for _ in X:
            Y.append([lev[0],lev[1]-lev[0]])
    else:
        for _ in X:
            Y.append([lat[0],lat[1]-lat[0]])
        if len(lat) > 2:
            Y.append([lat[2],lat[3]-lat[2]])
            Y.append([lat[2],lat[3]-lat[2]])
            X.extend(X)

    for x,y in zip(X,Y):
        patches.append(
            Rectangle((x[0],y[0]),
                       x[1],
                       y[1],
                       fill=False,
                       ls='--',
                       color='red'))
    return patches

files=['4co2_fix_tsurf_p_afr_la',
       '4co2_fix_tsurf_p_ama_la',
       '4co2_fix_tsurf_p_atl_la',
       '4co2_fix_tsurf_p_ind_la',
       '4co2_fix_tsurf_p_pac_la',
       
       '4co2_fix_tsurf_p_ama_ma',
       '4co2_fix_tsurf_p_atl_ma',
       '4co2_fix_tsurf_p_ind_ma',
       '4co2_fix_tsurf_p_pac_ma',
       
       '4co2_fix_tsurf_p_afr_ha',
       '4co2_fix_tsurf_p_ama_ha',
       '4co2_fix_tsurf_p_atl_ha',
       '4co2_fix_tsurf_p_ind_ha',
       '4co2_fix_tsurf_p_pac_ha',

       '4co2_fix_tsurf_m_afr_la',
       '4co2_fix_tsurf_m_ama_la',
       '4co2_fix_tsurf_m_atl_la',
       '4co2_fix_tsurf_m_ind_la',
       '4co2_fix_tsurf_m_pac_la',
       
       '4co2_fix_tsurf_m_afr_ma',
       '4co2_fix_tsurf_m_ind_ma',
       '4co2_fix_tsurf_m_pac_ma',

    ]

mlev = {"la":[1,7],
        "ma":[7,13],
        "ha":[13,19],
        "ta":[19,25]}
plev = {"la":[1000,890],
        "ma":[870,630],
        "ha":[630,400],
        "ta":[400,200]}
lat = {"pac":[-20,20],
       "ama":[-20,20],
       "atl":[-20,20],
       "afr":[-20,20],
       "ind":[-20,20],
       "equa":[-10,10],
       "extr":[-90,-35,35,90],
       "global":[-90,90]}
lon = { "pac":[165,255],
        "ama":[255,345],
        "atl":[288.75,356.25,18.75],
        "afr":[341.25,356.25,71.25],
        "ind":[33.75,123.75],
        "equa":[0,360],
        "extr":[0,360],
        "global":[0,360]}

nyears=20

for file in files:
    filespec=file.split('_')   
    if filespec[1] == 'fix': # 4CO2 fixed tsurf
        out_folder='/g/data/w40/dm5220/data/figures/fix_tsurf_tac_rad'
        change,area,atm=filespec[3:]
        ctl=my.UM.read_data('4co2_fix_tsurf')
        d=my.UM.read_data(file)
    elif filespec[1] == 'sw-': # 4CO2 SW-
        out_folder='/g/data/w40/dm5220/data/figures/tac_rad_test'
        change,area,atm=filespec[2:]
        ctl=my.UM.read_data('4co2_sw_x0.9452_offset')
        d=my.UM.read_data(file)
    else:
        raise Exception('Current script only works for 4co2_fix_tsurf or 4co2_sw- experiments.')
    
    changespec='_'.join([change,area,atm])
    anom=lambda var: d[var]-ctl[var]
    p=lambda var: d[var].t_student_probability(ctl[var],num_years=nyears)

    def plot_level(var,mean,func=lambda x: x*1,**kwargs):
        P=p(var)
        data=func(anom(var)).annual_mean(12*nyears,normalize=True)
        if 'pressure' in data.dims:
            levs=plev
        else:
            levs=mlev

        if mean == 'lonmean':
            selection=sel_lon
            rec=rectangle(lev=levs[atm],lat=lat[area])
        else:
            selection=sel_lat
            rec=rectangle(lev=levs[atm],lon=lon[area])

        if 'outpath' in kwargs:
            outpath=kwargs.pop('outpath')
            save=True
        else:
            save=False

        data=selection(data)
        data.plotlev(
            t_student=selection(P),
            double_axis=True,
            **kwargs)
        for r in rec:
            plt.gca().add_patch(r)
        if save:
            plt.savefig(outpath, dpi=300, bbox_inches='tight')

    def plot(var,func=lambda x: x*1,**kwargs):
        rec=rectangle(lon=lon[area],lat=lat[area])
        if 'outpath' in kwargs:
            outpath=kwargs.pop('outpath')
            save=True
        else:
            save=False
        P=p(var)
        data=func(anom(var)).annual_mean(12*nyears,normalize=True)
        data.plotvar(
            t_student=P,
            **kwargs)
        for r in rec:
            plt.gca().add_patch(r)
        if save:
            plt.savefig(outpath, dpi=300, bbox_inches='tight')

    def plot_profile(var,func=lambda x: x*1,**kwargs):
        if 'outpath' in kwargs:
            outpath=kwargs.pop('outpath')
            save=True
        else:
            save=False
        data=func(anom(var))
        data=sel_lat(sel_lon(data))
        if 'pressure' in data.dims:
            levs=plev
        else:
            levs=mlev
        data.plotprof(
            timesteps=12*nyears,
            double_axis=True,
            normalize=True,
            **kwargs)
        xlim=plt.gca().get_xlim()
        plt.hlines(levs[atm][0],*xlim,color='red',lw=1,ls='--')
        plt.hlines(levs[atm][1],*xlim,color='red',lw=1,ls='--')
        if save:
            plt.savefig(outpath, dpi=300, bbox_inches='tight')

    plt_levels=np.linspace(-1,1,20)
    plt_du=0.25
    
    # TSURF 
    var='surface_temperature'
    plt.figure()
    plot(var,
        levels=plt_levels,      du=0.25,
        units='$K/K$',
        cmap=my.Colormaps.div_tsurf,
        title=f'Surface Temperature | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_tsurf'))
    plt.clf()

    # PRECIP
    var='precipitation_flux'
    plot(var,
        func=lambda x: x.to_mm_per_day(),
        levels=plt_levels,      du=0.25,
        units='$(mm \cdot d^{-1})/(mm \cdot d^{-1})$',
        cmap=my.Colormaps.div_precip,
        title=f'Precipitation | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_precip'))
    plt.clf()

    # TAIR 
    # plev (lonmean)
    var='air_temperature_0_plev'
    plot_level(var,'lonmean',
        levels=plt_levels,
        du=plt_du,
        units='$K/K$',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_tair_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',
        levels=plt_levels,
        du=plt_du,
        units='$K/K$',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_tair_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='air_temperature_0'
    plot_level(var,'lonmean',
        levels=plt_levels,
        du=plt_du,
        units='$K/K$',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_tair_lonmean_mlev'))
    plt.clf()
    # mlev (latmean)
    plot_level(var,'latmean',
        levels=plt_levels,
        du=plt_du,
        units='$K/K$',
        cmap=my.Colormaps.div_tsurf,
        title=f'Air Temperature | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_tair_latmean_mlev'))
    plt.clf()

    # LW HEATIING RATES
    # plev (lonmean)
    var='tendency_of_air_temperature_due_to_longwave_heating_plev'
    plot_level(var,'lonmean',func=lambda x: x.to_K_per_day(),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_LWhrate_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',func=lambda x: x.to_K_per_day(),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_LWhrate_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='tendency_of_air_temperature_due_to_longwave_heating'
    plot_level(var,'lonmean',func=lambda x: x.to_K_per_day(force=True),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_LWhrate_lonmean_mlev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',func=lambda x: x.to_K_per_day(force=True),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'LW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_LWhrate_latmean_mlev'))
    plt.clf()

    # SW HEATIING RATES
    # plev (lonmean)
    var='tendency_of_air_temperature_due_to_shortwave_heating_plev'
    plot_level(var,'lonmean',func=lambda x: x.to_K_per_day(),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_SWhrate_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',func=lambda x: x.to_K_per_day(),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_SWhrate_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='tendency_of_air_temperature_due_to_shortwave_heating'
    plot_level(var,'lonmean',func=lambda x: x.to_K_per_day(force=True),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_SWhrate_lonmean_mlev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',func=lambda x: x.to_K_per_day(force=True),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'SW Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_SWhrate_latmean_mlev'))
    plt.clf()

    # TOT HEATIING RATES
    # plev (lonmean)
    var='tendency_of_air_temperature_due_to_total_heating_plev'
    plot_level(var,'lonmean',func=lambda x: x.to_K_per_day(),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_TOThrate_lonmean_plev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',func=lambda x: x.to_K_per_day(),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_TOThrate_latmean_plev'))
    plt.clf()
    # mlev (lonmean)
    var='tendency_of_air_temperature_due_to_total_heating'
    plot_level(var,'lonmean',func=lambda x: x.to_K_per_day(force=True),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_TOThrate_lonmean_mlev'))
    plt.clf()
    # plev (latmean)
    plot_level(var,'latmean',func=lambda x: x.to_K_per_day(force=True),
        levels=plt_levels,
        du=plt_du,
        units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
        cmap=my.Colormaps.div_tsurf,
        title=f'TOT Heating Rate | {changespec}',
        outpath=os.path.join(out_folder,f'{changespec}_TOThrate_latmean_mlev'))
    plt.clf()

    # TAIR VERTICAL PROFILE
    # plev
    var='air_temperature_0_plev'
    plot_profile(var,
                xlim=[-5,3],
                dx=1,
                units='$K/K$',
                title=f'Air Temperature | {changespec}',
                outpath=os.path.join(out_folder,f'{changespec}_tair_vertprof_plev'))
    plt.clf()
    # mlev
    var='air_temperature_0'
    plot_profile(var,
                xlim=[-5,3],
                dx=1,
                units='$K/K$',
                title=f'Air Temperature | {changespec}',
                outpath=os.path.join(out_folder,f'{changespec}_tair_vertprof_mlev'))
    plt.clf()

    # TOT HRATE VERTICAL PROFILE
    # plev
    var='tendency_of_air_temperature_due_to_total_heating_plev'
    plot_profile(var,
                func=lambda x: x.to_K_per_day(force=True),
                xlim=[-0.4,0.4],
                dx=0.1,
                units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
                title=f'TOT Heating Rate | {changespec}',
                outpath=os.path.join(out_folder,f'{changespec}_TOThrate_vertprof_plev'))
    plt.clf()
    # mlev
    var='tendency_of_air_temperature_due_to_total_heating'
    plot_profile(var,
                func=lambda x: x.to_K_per_day(force=True),
                xlim=[-0.4,0.4],
                dx=0.1,
                units='$(K \cdot d^{-1})/(K \cdot d^{-1})$',
                title=f'TOT Heating Rate | {changespec}',
                outpath=os.path.join(out_folder,f'{changespec}_TOThrate_vertprof_mlev'))
    plt.clf()
