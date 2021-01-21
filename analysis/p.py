import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np

input_folder="/g/data/w48/dm5220/data"
alpha_precip=86400
output_folder=input_folder+"/figures/tair_change"

ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"tac_control/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))                      

def anomalies(data,var="air_temperature",data_ctl=tac_ctl,a=1,t=True,**kwargs):
    kwargs_pred={}
    if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-6,6,50)
    if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Constants.colormaps.div_tsurf
    if "cbar_kwargs" not in kwargs: kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-6,6+1,1)}
    if var in ["precipitation_flux"]: a=alpha_precip
    d=data[var]*a
    ctl=data_ctl[var]*a
    if len(d.shape) == 4:
        if t: t=my.DataArray(d.mean("longitude_0")).t_student_probability(ctl.mean("longitude_0"))
        mean=lambda x: x.mean(["time","longitude_0"])
        fun=lambda x:x.plotlev(**kwargs_pred,t_student=t,**kwargs)
    elif len(d.shape) == 3:
        if t: t=my.DataArray(d).t_student_probability(ctl)
        mean=lambda x: x.mean(["time"])
        fun=lambda x:x.plotvar(**kwargs_pred,t_student=t,**kwargs)
    else:
        raise Exception("Data shape mismatching!")
    fun(my.DataArray((mean(d)-mean(ctl))))

co2x4 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_4co2 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_nc/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))                    
fix=my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_4co2_offset = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_4co2_tac_offset/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_4co2_offset_2 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_4co2_tac_offset_2/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_4co2_offset_3 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_4co2_tac_offset_3/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_4co2_offset_4 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_4co2_tac_offset_4/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))                                 
tac_4co2_offset_5 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_4co2_tac_offset_5/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))                                            
# tac_4co2_offset_6 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_4co2_tac_offset_6/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                                            
# test_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_control/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                      

