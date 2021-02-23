import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
from cftime import Datetime360Day as dt360
import datetime as dt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import matplotlib.cm as cm
from scipy.stats import pearsonr as corr
from scipy.signal import correlate2d as corr2d

#%%
input_folder="/g/data/w48/dm5220/data"
alpha_precip=86400

def new_name(x):
    return x.rename_vars({"m01s09i231":"combined_cloud_amount"})

ctl = new_name(my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"ctl/*_pa*.nc"),
           concat_dim="time",parallel=True)))
co2x4 = new_name(my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2/*_pa*.nc"),
           concat_dim="time",parallel=True)))
fix = new_name(my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_fix_tsurf/*_pa*.nc"),
           concat_dim="time",parallel=True)))
solar_up_fix = new_name(my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"ctl_fix_tsurf_solar50+/*_pa*.nc"),
           concat_dim="time",parallel=True)))
solar_down_4co2 = new_name(my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_solar50-/*_pa*.nc"),
           concat_dim="time",parallel=True)))                              
ctl_fix = new_name(my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"ctl_fix_tsurf/*_pa*.nc"),
           concat_dim="time",parallel=True)))                              

ctl_2 = xr.open_mfdataset(os.path.join(input_folder,"old_experiments/ctl/*_pa*.nc"),
           concat_dim="time",parallel=True)

solar = xr.open_mfdataset(os.path.join(input_folder,"old_experiments/control_solar_plus50W/*_pa*.nc"),
           concat_dim="time",parallel=True)

def anomalies(data,var="air_temperature",control=ctl,a=1,t=True,**kwargs):
    kwargs_pred={}
    if var in ["air_temperature","air_temperature_0","surface_temperature"]:
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-3,3,100)
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Constants.colormaps.div_tsurf
        if ("add_colorbar" not in kwargs) and ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-3,3+1,1),"label":"°C"}
    elif var in ["precipitation_flux","deep_convective_precipitation_rate","mid_level_convective_precipitation_rate","shallow_convective_precipitation_rate"]: 
        a=alpha_precip
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-2,2,100)
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Constants.colormaps.div_precip        
        if ("add_colorbar" not in kwargs) and ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-2,2+0.5,0.5), "label":"mm/day"}
    elif var in ["high_type_cloud_area_fraction","low_type_cloud_area_fraction","medium_type_cloud_area_fraction"]: 
        if "cmap" not in kwargs: kwargs_pred["cmap"]=cm.PRGn
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-0.2,0.2,100)                        
        if ("add_colorbar" not in kwargs) and ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-0.2,0.2+0.05,0.05),"label":None}
    elif var in ["m01s09i231", "combined_cloud_amount"]: 
        if "title" not in kwargs: kwargs_pred["title"]=""
        if "cmap" not in kwargs: kwargs_pred["cmap"]=cm.PRGn
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-0.02,0.02,100)                        
        if ("add_colorbar" not in kwargs) and ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-0.02,0.02+0.005,0.005),"label":None}
    # select just last 30 years
    sel=lambda x: x.isel(time=slice(-12*30,None))
    d=my.DataArray(sel(data[var]*a))
    data_ctl=my.DataArray(sel(control[var]*a))
    lat0,lon0=data_ctl.get_spatial_coords()
    lat,lon=d.get_spatial_coords()
    if len(d.shape) == 4:
        if t: t=d.mean(lon).t_student_probability(data_ctl.mean(lon0))
        mean=lambda x: x.mean(["time",x.get_spatial_coords()[1]])
        fun=lambda x:x.plotlev(**kwargs_pred,t_student=t,**kwargs)
    elif len(d.shape) == 3:
        if t: t=d.t_student_probability(data_ctl)
        mean=lambda x: x.mean(["time"])
        fun=lambda x:x.plotvar(**kwargs_pred,t_student=t,**kwargs)
    else:
        raise Exception("Data shape mismatching!")
    return fun((mean(d)-mean(data_ctl)))

def seasonal_cycle(data,var="air_temperature",a=1,**kwargs):
    kwargs_pred={}
    if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-3,3,50)
    if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Constants.colormaps.div_tsurf
    if ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-3,3+0.5,0.5)}
    if var in ["precipitation_flux"]: 
        a=alpha_precip
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Constants.colormaps.div_precip
    sel=lambda x: x.isel(time=slice(-12*30,None))        
    d=sel(data[var]*a)
    data_ctl=sel(ctl[var]*a)
    if len(d.shape) == 4:
        # if t: t=my.DataArray(d.mean("longitude_0")).t_student_probability(data_ctl.mean("longitude_0"))
        seascyc=lambda x: my.DataArray(x.mean("longitude_0")).seasonal_cycle()
        fun=lambda x:x.plotlev(**kwargs_pred,**kwargs)
    elif len(d.shape) == 3:
        # if t: t=my.DataArray(d).t_student_probability(data_ctl)
        seascyc=lambda x: my.DataArray(x).seasonal_cycle()
        fun=lambda x:x.plotvar(**kwargs_pred,**kwargs)
    else:
        raise Exception("Data shape mismatching!")
    fun(seascyc(d-data_ctl))  

def annual_cycle(data,var="precipitation_flux",a=alpha_precip,**kwargs):
    if var in ["surface_temperature"]: 
        a=1
    sel=lambda x: x.isel(time=slice(-12*30,None))        
    d=sel(data[var]*a)
    data_ctl=sel(ctl[var]*a)
    if len(d.shape) == 3:
        anncyc=lambda x: my.DataArray(x).global_mean().annual_cycle().assign_coords({"time":np.arange(1,13)})
        def fun(x):
            x.plot(**kwargs)
            plt.ylim([-0.2,0.2])
            plt.title("Annual Cycle")
            plt.xlabel(None)
            plt.gca().set_xticks(np.arange(1,13,dtype=int))
            plt.gca().set_xticklabels(["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"],
                                      fontsize=9)
    else:
        raise Exception("Annual Cycle can only be computed for 3D variables (time,lat,lon).")
    fun(anncyc(d-data_ctl)) 

def time_series(data,var="surface_temperature",a=1,moving_average=24,**kwargs):
    if var in ["precipitation_flux"]: 
        a=alpha_precip
    d=data[var]*a
    data_ctl=ctl[var]*a
    time_series=my.DataArray(d-data_ctl).global_mean()
    if len(time_series.shape) == 2:
        dim=[x for x in a.dims if x != "time"][0]
        time_series=time_series.mean(dim)
    if moving_average is not None:
        time_series=time_series.rolling(time=moving_average, center=True, min_periods=2).mean()
    def fun(x):
        n=len(x.time)
        x2=x.isel(time=slice(-12*30,None))
        x1=x.isel(time=slice(0,12*20,None)) 
        x2.plot(**kwargs)
        if "label" in kwargs: del kwargs["label"]
        if ("linewidth" in kwargs): del kwargs["linewidth"]
        x1.plot(**kwargs,linestyle="dashed",label=None,linewidth=0.8)
        gm=x2.mean() 
        c = kwargs.pop("color") if "color" in kwargs else None 
        plt.axhline(y = gm, color=c, **kwargs,linestyle = '-.',linewidth=0.5) 
        # plt.ylim([-1,3])
        plt.title("Time Series")
        plt.xlabel("Years")
        plt.gca().set_xticks(np.arange(0,n+12*5,12*5))
        plt.gca().set_xticklabels(np.arange(0,n/12+5,5,dtype=int))
    fun(time_series.assign_coords({"time":np.arange(1,len(time_series.time)+1)}))

def vertical_profile(data,var="air_temperature",a=1,**kwargs):
    # select just last 30 years
    sel=lambda x: x.isel(time=slice(-12*30,None),pressure=slice(2,None))
    d=sel(data[var]*a)
    data_ctl=sel(ctl[var]*a)
    if len(d.shape) == 4:
        vert=mean(d-data_ctl)
    else:
        raise Exception("Data shape mismatching!")
    def fun(x):
        yinc=kwargs.pop("yincrease") if "yincrease" in kwargs else False
        ysc=kwargs.pop("yscale") if "yscale" in kwargs else "log"
        x.plot(y="pressure",**kwargs,yincrease=yinc,yscale=ysc)
        plt.ylim([1000,50])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(["{}".format(i) for i in [1000,800,600,400,200,50]])
    fun(vert)

def convection_rate(data,**kwargs):
    tit=kwargs.pop("title") if "title" in kwargs else None
    kwargs_pred={"add_colorbar":False,"statistics":['all',7],
                 "levels":np.linspace(-1.5,1.5,50),
                 "cmap":my.Constants.colormaps.div_precip}
    for k in kwargs_pred:
        if k in kwargs: del kwargs_pred[k]                  
    gs = gridspec.GridSpec(3, 4, height_ratios=[10, 10, 2],
                    hspace=0.55, wspace=0.1)
    ax1 = plt.subplot(gs[0, 0:2],projection=ccrs.Robinson())
    im=anomalies(data,var="deep_convective_precipitation_rate",
                ax=ax1, **kwargs_pred, title="Deep Convective Rainfall",**kwargs)
    ax2 = plt.subplot(gs[0, 2:],projection=ccrs.Robinson())
    anomalies(data,var="mid_level_convective_precipitation_rate",
              ax=ax2, **kwargs_pred, title="Mid-level Convective Rainfall",**kwargs)
    ax3 = plt.subplot(gs[1, 1:3],projection=ccrs.Robinson())
    anomalies(data,var="shallow_convective_precipitation_rate",
              ax=ax3, **kwargs_pred, title="Shallow Convective Rainfall",**kwargs)              
    axc = plt.subplot(gs[2, :])
    plt.colorbar(im,cax=axc, orientation='horizontal',
                 ticks=np.arange(-1.5,1.5+0.5,0.5),label="mm/day")
    plt.suptitle(tit,fontsize=14)

def convective_clouds(data,**kwargs):
    tit=kwargs.pop("title") if "title" in kwargs else None
    kwargs_pred={"add_colorbar":False,"statistics":['all',7],
                 "levels":np.linspace(-0.2,0.2,50),
                 "cmap":cm.PRGn}
    for k in kwargs_pred:
        if k in kwargs: del kwargs_pred[k]                  
    gs = gridspec.GridSpec(3, 4, height_ratios=[10, 10, 2],
                    hspace=0.55, wspace=0.1)
    ax1 = plt.subplot(gs[0, 0:2],projection=ccrs.Robinson())
    im=anomalies(data,var="high_type_cloud_area_fraction",
                ax=ax1, **kwargs_pred, title="High Convective Clouds",**kwargs)
    ax2 = plt.subplot(gs[0, 2:],projection=ccrs.Robinson())
    anomalies(data,var="medium_type_cloud_area_fraction",
              ax=ax2, **kwargs_pred, title="Medium Convective Clouds",**kwargs)
    ax3 = plt.subplot(gs[1, 1:3],projection=ccrs.Robinson())
    anomalies(data,var="low_type_cloud_area_fraction",
              ax=ax3, **kwargs_pred, title="Low Convective Clouds",**kwargs)              
    axc = plt.subplot(gs[2, :])
    plt.colorbar(im,cax=axc, orientation='horizontal',
                 ticks=np.arange(-0.2,0.2+0.05,0.05),label=None)
    plt.suptitle(tit,fontsize=14)

def correlation(data,var1="precipitation_flux",var2="high_type_cloud_area_fraction",title=None):
    gs = gridspec.GridSpec(1, 2, wspace=0.1)
    fig=plt.figure()
    ax1 = plt.subplot(gs[0, 0],projection=ccrs.Robinson())
    anomalies(data,var=var1,ax=ax1,statistics=['all',7])
    # for t in cb.ax.get_yticklabels():
    #     t.set_fontsize(7)
    ax2 = plt.subplot(gs[0, 1],projection=ccrs.Robinson())
    anomalies(data,var=var2,ax=ax2,statistics=['all',7])
    fig.title(title,y=0.9)

#%%
datas=(co2x4,ctl_fix,fix,solar_up_fix,solar_down_4co2)
labels=("4co2","ctl + fix ctl","4co2 + fix ctl","fix ctl + solar 50+","4co2 + solar 50-")
colors=("blue","darkorchid","orange","green","red")

#%%
# # PLOT CONVECTIVE CLOUDS 
# for d,l in zip(datas,labels):
#     plt.figure()
#     convective_clouds(d,title="{}".format(l))

#%%
# # PLOT CONVECTIVE PRECIPITATION 
# for d,l in zip(datas,labels):
#     plt.figure()
#     convection_rate(d,title="{}".format(l))

#%%
# PLOT ANNUAL MEAN ANOMALIES 
# SURFACE TEMPERATURE
for d,l in zip(datas,labels):
    plt.figure()
    anomalies(d,var="surface_temperature",title="Surface Temperature | {}".format(l))
# PRECIPITATION
for d,l in zip(datas,labels):
    plt.figure()
    anomalies(d,var="precipitation_flux",title="Precipitation | {}".format(l))
# # AIR TEMPERATURE
for d,l in zip(datas,labels):
    plt.figure()
    anomalies(d,title="Air Temperature | {}".format(l))
# # DEEP CONVECTIVE PRECIPITATION
# for d,l in zip(datas,labels):
#     plt.figure()
#     anomalies(d,title="Deep Convective Precipitation | {}".format(l),
#               var="deep_convective_precipitation_rate",
#               levels=np.linspace(-1.5,1.5,50))
# # MID-LEVEL CONVECTIVE PRECIPITATION
# for d,l in zip(datas,labels):
#     plt.figure()
#     anomalies(d,title="Mid-level Convective Precipitation | {}".format(l),
#               var="mid_level_convective_precipitation_rate",
#               levels=np.linspace(-1.5,1.5,50))
# # SHALLOW CONVECTIVE PRECIPITATION
# for d,l in zip(datas,labels):
#     plt.figure()
#     anomalies(d,title="Shallow Convective Precipitation | {}".format(l),
#               var="shallow_convective_precipitation_rate",
#               levels=np.linspace(-1.5,1.5,50))
# # DEEP CONVECTIVE CLOUDS
# for d,l in zip(datas,labels):
#     plt.figure()
#     anomalies(d,title="High Convective Clouds | {}".format(l),
#               var="high_type_cloud_area_fraction")
# # MEDIUM CONVECTIVE CLOUDS
# for d,l in zip(datas,labels):
#     plt.figure()
#     anomalies(d,title="Medium Convective Clouds | {}".format(l),
#               var="medium_type_cloud_area_fraction")
# # LOW CONVECTIVE CLOUDS
# for d,l in zip(datas,labels):
#     plt.figure()
#     anomalies(d,title="Low Convective Clouds | {}".format(l),
#               var="low_type_cloud_area_fraction")

# AIR TEMPERATURE
# %%
# # PLOT PRECIPITATION ANNUAL CYCLES
# plt.figure()
# for d,l,c in zip(datas,labels,colors):
#     annual_cycle(d,var="precipitation_flux",label=l,color=c)
# plt.legend()
# plt.grid()


#%%
# # PLOT TIME SERIES
# # TSURF
# plt.figure()
# for d,l,c in zip(datas,labels,colors):
#     time_series(d,label=l,color=c)
# plt.legend(prop={'size': 8})
# plt.grid()
# # PRECIPITATION
# plt.figure()
# for d,l,c in zip(datas,labels,colors):
#     time_series(d,var="precipitation_flux",label=l,color=c)
# plt.legend(prop={'size': 8},loc='lower left',
#            bbox_to_anchor=(0.1, 0.23))
# plt.grid()

# %%
# # # PLOT VERTICAL PROFILES
# for d,l,c in zip(datas,labels,colors):
#     vertical_profile(d,color=c,label=l)
# plt.title("Vertical Levels")    
# plt.grid()
# plt.legend()

# %%
# # ESTIMATE NOISE
# var="precipitation_flux"
# s1=lambda x: x[var].isel(time=slice(-10*12,None)).mean("time")
# s2=lambda x: x[var].isel(time=slice(-30*12,-20*12)).mean("time")
# plt.figure()
# my.DataArray((s1(ctl)-s2(ctl))*alpha_precip).plotvar(title="ctl",
#             levels=np.linspace(-1,1,50),cmap=my.Constants.colormaps.div_precip)
# plt.figure()
# my.DataArray((s1(ctl_fix)-s2(ctl_fix))*alpha_precip).plotvar(title="ctl_fix",
#             levels=np.linspace(-1,1,50),cmap=my.Constants.colormaps.div_precip)
