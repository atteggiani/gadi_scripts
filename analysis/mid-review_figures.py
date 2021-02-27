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
import gc
import time

input_folder="/g/data/w48/dm5220/data"
output_folder="/g/data/w48/dm5220/data/mid_review_figures"
alpha_precip=86400

ctl = my.open_mfdataset(os.path.join(input_folder,"ctl/*_pa*.nc"),
           concat_dim="time",parallel=True)
co2x4 = my.open_mfdataset(os.path.join(input_folder,"4co2/*_pa*.nc"),
           concat_dim="time",parallel=True)
co2x4_fix = my.open_mfdataset(os.path.join(input_folder,"4co2_fix_tsurf/*_pa*.nc"),
           concat_dim="time",parallel=True)
solar_up = my.open_mfdataset(os.path.join(input_folder,"ctl_solar50+/*_pa*.nc"),
           concat_dim="time",parallel=True)        
solar_up_fix = my.open_mfdataset(os.path.join(input_folder,"ctl_fix_tsurf_solar50+/*_pa*.nc"),
           concat_dim="time",parallel=True)     
co2x4_solar_down = my.open_mfdataset(os.path.join(input_folder,"4co2_solar50-/*_pa*.nc"),
           concat_dim="time",parallel=True)                            
ctl_fix = my.open_mfdataset(os.path.join(input_folder,"ctl_fix_tsurf/*_pa*.nc"),
           concat_dim="time",parallel=True)                          

def anomalies(data,var="air_temperature",control=ctl,a=1,t=True,**kwargs):
    kwargs_pred={}
    if var in ["air_temperature","air_temperature_0","surface_temperature"]:
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-3,3,100)
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Colormaps.div_tsurf
        if ("add_colorbar" not in kwargs) and ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-3,3+1,1),"label":"°C"}
    elif var in ["precipitation_flux","deep_convective_precipitation_rate","mid_level_convective_precipitation_rate","shallow_convective_precipitation_rate"]: 
        a=alpha_precip
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-2,2,100)
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Colormaps.div_precip        
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
    elif var in ["omega_up", "omega_down"]: 
        if "title" not in kwargs: kwargs_pred["title"]=""
        if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-0.005,0.005,100)                        
        if ("add_colorbar" not in kwargs) and ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-0.005,0.005+0.0025,0.0025),"label":None}
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Colormaps.div_precip if var == "omega_up" else my.Colormaps.div_precip_r
    # select just last 30 years
    sel=lambda x: x.isel(time=slice(-12*30,None))
    d=my.DataArray(sel(data[var]*a))
    data_ctl=my.DataArray(sel(control[var]*a))
    lat0,lon0=data_ctl.get_spatial_coords()
    lat,lon=d.get_spatial_coords()
    if var in ["omega_up", "omega_down"]: 
        d=d.sel({"pressure":500},method="nearest")
        data_ctl=data_ctl.sel({"pressure":500},method="nearest")
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
    if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Colormaps.div_tsurf
    if ("cbar_kwargs" not in kwargs) and ("levels" not in kwargs): kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-3,3+0.5,0.5)}
    if var in ["precipitation_flux"]: 
        a=alpha_precip
        if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Colormaps.div_precip
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

def time_series(data,var="surface_temperature",a=1,moving_average=60,**kwargs):
    if var in ["precipitation_flux"]: 
        a=alpha_precip
    d=data[var]*a
    data_ctl=ctl[var]*a
    if var in ["omega_up","omega_down"]: 
        d=d.sel({"pressure":500},method="nearest")
        data_ctl=data_ctl.sel({"pressure":500},method="nearest")
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
        vert=my.DataArray(d-data_ctl).annual_mean().global_mean()
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




datas=(co2x4,solar_up,co2x4_fix,solar_up_fix,co2x4_solar_down,ctl_fix)
labels=("4xCO2","Solar +50","4xCO2 + FIX","Solar +50 + FIX","4xCO2 + Solar -50","Control + FIX")
colors=("black","red","grey","orange","green","blue")
out=("4co2","solar_up","4co2_fix","solar_up_fix","4co2_solar_down","ctl_fix")



# PLOT ANNUAL MEAN ANOMALIES 
# SURFACE TEMPERATURE
for d,l,o in zip(datas,labels,out):
    plt.figure()
    anomalies(d,var="surface_temperature",title="Surface Temperature | {}".format(l),
              outpath=os.path.join(output_folder,"tsurf_{}.png".format(o)))
    plt.show();plt.close() 
# PRECIPITATION
for d,l,o in zip(datas,labels,out):
    plt.figure()
    anomalies(d,var="precipitation_flux",title="Precipitation | {}".format(l),
              outpath=os.path.join(output_folder,"precip_{}.png".format(o)))
    plt.show();plt.close() 
# AIR TEMPERATURE
for d,l,o in zip(datas,labels,out):
    plt.figure()
    anomalies(d,var="air_temperature",title="Air Temperature | {}".format(l),
              outpath=os.path.join(output_folder,"tair_{}.png".format(o)))    
    plt.show();plt.close() 
# OMEGA UP
for d,l,o in zip(datas,labels,out):
    plt.figure()
    anomalies(d,var="omega_up",title="Omega Up (500hPa) | {}".format(l),
              outpath=os.path.join(output_folder,"w_up_{}.png".format(o)))    
    plt.show();plt.close() 
# OMEGA DOWN
for d,l,o in zip(datas,labels,out):
    plt.figure()
    anomalies(d,var="omega_down",title="Omega Down (500hPa) | {}".format(l),
              outpath=os.path.join(output_folder,"w_down_{}.png".format(o)))                                        
    plt.show();plt.close() 



# PLOT TIME SERIES
# TSURF
plt.figure()
for d,l,c in zip(datas[:-2],labels[:-2],colors[:-2]):
    time_series(d,label=l,color=c,moving_average=60)
plt.legend(prop={'size': 10})
plt.title("Surface temperature | Time Series",fontsize=14)
plt.grid()
plt.ylabel("°C")
plt.savefig(os.path.join(output_folder,"tsurf_tseries_1.png"),bbox_to_anchor="tight",dpi=300)
# PRECIPITATION
plt.figure()
for d,l,c in zip(datas[:-2],labels[:-2],colors[:-2]):
    time_series(d,var="precipitation_flux",label=l,color=c,moving_average=60)
plt.legend(prop={'size': 10},loc='upper left',
           bbox_to_anchor=(0.01, 0.99))
plt.title("Precipitation | Time Series",fontsize=14)           
plt.ylabel("mm/day")
plt.grid()
plt.savefig(os.path.join(output_folder,"precip_tseries_1.png"),bbox_to_anchor="tight",dpi=300)
# OMEGA UP
plt.figure()
for d,l,c in zip(datas[:-2],labels[:-2],colors[:-2]):
    time_series(d,var="omega_up",label=l,color=c,moving_average=60)
plt.legend(prop={'size': 10})
plt.title("Omega Up (500hPa) | Time Series",fontsize=14)           
plt.ylabel("m/s")
plt.grid()
plt.savefig(os.path.join(output_folder,"w_up_tseries_1.png"),bbox_to_anchor="tight",dpi=300)

# PLOT TIME SERIES
# TSURF
plt.figure()
for d,l,c in zip(datas[-2:],labels[-2:],colors[-2:]):
    time_series(d,label=l,color=c,moving_average=60)
plt.legend(prop={'size': 10})
plt.title("Surface temperature | Time Series",fontsize=14)
plt.grid()
plt.ylabel("°C")
plt.ylim([-0.5,0.5])
plt.savefig(os.path.join(output_folder,"tsurf_tseries_2.png"),bbox_to_anchor="tight",dpi=300)
# PRECIPITATION
plt.figure()
for d,l,c in zip(datas[-2:],labels[-2:],colors[-2:]):
    time_series(d,var="precipitation_flux",label=l,color=c,moving_average=60)
plt.legend(prop={'size': 10})
plt.title("Precipitation | Time Series",fontsize=14)           
plt.ylabel("mm/day")
plt.grid()
plt.savefig(os.path.join(output_folder,"precip_tseries_2.png"),bbox_to_anchor="tight",dpi=300)
# OMEGA UP
plt.figure()
for d,l,c in zip(datas[-2:],labels[-2:],colors[-2:]):
    time_series(d,var="omega_up",label=l,color=c,moving_average=60)
plt.legend(prop={'size': 10})
plt.title("Omega Up (500hPa) | Time Series",fontsize=14)           
plt.ylabel("m/s")
plt.grid()
plt.ylim([-1e-4,1e-4])
plt.savefig(os.path.join(output_folder,"w_up_tseries_2.png"),bbox_to_anchor="tight",dpi=300)




# # PLOT TAIR VERTICAL PROFILES
plt.figure()
for d,l,c in zip(datas[:-2],labels[:-2],colors[:-2]):
    vertical_profile(d,var="air_temperature",color=c,label=l)
plt.title("Air temperature | Vertical profile",fontsize=14)    
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"tair_vertical_profile_1.png"),bbox_to_anchor="tight",dpi=300)

# # PLOT TAIR VERTICAL PROFILES
plt.figure()
for d,l,c in zip(datas[-2:],labels[-2:],colors[-2:]):
    vertical_profile(d,var="air_temperature",color=c,label=l)
plt.title("Air temperature | Vertical profile",fontsize=14)    
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"tair_vertical_profile_2.png"),bbox_to_anchor="tight",dpi=300)




# # PLOT omega_up VERTICAL PROFILES
plt.figure()
for d,l,c in zip(datas[:-2],labels[:-2],colors[:-2]):
    vertical_profile(d,var="omega_up",color=c,label=l)
plt.title("Omega up | Vertical profile",fontsize=14)    
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"w_up_vertical_profile_1.png"),bbox_to_anchor="tight",dpi=300)

# # PLOT omega_up VERTICAL PROFILES
plt.figure()
for d,l,c in zip(datas[-2:],labels[-2:],colors[-2:]):
    vertical_profile(d,var="omega_up",color=c,label=l)
plt.title("Omega up | Vertical profile",fontsize=14)    
plt.grid()
plt.legend()
plt.savefig(os.path.join(output_folder,"w_up_vertical_profile_2.png"),bbox_to_anchor="tight",dpi=300)

# %%


