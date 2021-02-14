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
tac_4co2 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_nc/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None)) 
tac_ctl_fix_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_fix_ctl_tac_nc/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None)) 
tac_4co2_fix_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_fix_ctl_tac_nc/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))            
# tac_4co2_offset = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_offset/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change1 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change1/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change2 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change2/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change3 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change3/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                                 
# tac_4co2_change4 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change4/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                                            
# tac_4co2_change6 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change6/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                                            
# tac_4co2_change7 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change7/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                                            
# tac_4co2_change10 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change10/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))                                            
# tac_4co2_change1_fix = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change1_fix/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change2_fix = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change2_fix/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change3_fix = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change3_fix/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change4_fix = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change4_fix/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
# tac_4co2_change5_fix = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_tac_change5_fix/*_pa*.nc"),
#            concat_dim="time",parallel=True)).isel(time=slice(120,None))
co2x4 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))           
test_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_control/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))                      
fix=my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/*_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))

def anomalies(data,var="air_temperature",data_ctl=tac_ctl,a=1,t=True,**kwargs):
    kwargs_pred={}
    if "levels" not in kwargs: kwargs_pred["levels"]=np.linspace(-3,3,50)
    if "cmap" not in kwargs: kwargs_pred["cmap"]=my.Constants.colormaps.div_tsurf
    if "cbar_kwargs" not in kwargs: kwargs_pred["cbar_kwargs"]={"ticks":np.arange(-3,3+0.5,0.5)}
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

# plt.figure(); anomalies(fix,data_ctl=ctl,
#                         title="4co2 fix | Air Temperature",
#                         outpath=output_folder+"/tair_4co2_fix.png")
# plt.figure(); anomalies(fix,data_ctl=ctl,
#                         title="4co2 fix | Surface Temperature",
#                         outpath=output_folder+"/tsurf_4co2_fix.png",
#                         var="surface_temperature")
# plt.figure(); anomalies(fix,data_ctl=ctl,
#                         title="4co2 fix | Precipitation",
#                         outpath=output_folder+"/precip_4co2_fix.png",
#                         var="precipitation_flux",
#                         cmap=my.Constants.colormaps.div_precip)

# plt.figure(); anomalies(tac_ctl_fix_ctl,
#                         title="ctl fix tac no-change | Air Temperature",
#                         outpath=output_folder+"/tair_ctl_fix_tac_nc.png")
# plt.figure(); anomalies(tac_ctl_fix_ctl,
#                         title="ctl fix tac no-change | Surface Temperature",
#                         outpath=output_folder+"/tsurf_ctl_fix_tac_nc.png",
#                         var="surface_temperature")
# plt.figure(); anomalies(tac_ctl_fix_ctl,
#                         title="ctl fix tac no-change | Precipitation",
#                         outpath=output_folder+"/precip_ctl_fix_tac_nc.png",
#                         var="precipitation_flux",
#                         cmap=my.Constants.colormaps.div_precip)

# plt.figure(); anomalies(tac_4co2_offset,
#                         title="4co2 tac change 0 | Air Temperature",
#                         outpath=output_folder+"/tair_4co2_tac_ch0.png")
# plt.figure(); anomalies(tac_4co2_offset,
#                         title="4co2 tac change 0 | Surface Temperature",
#                         outpath=output_folder+"/tair_4co2_tac_ch0.png",
#                         var="surface_temperature")
# plt.figure(); anomalies(tac_4co2_offset,
#                         title="4co2 tac change 0 | Precipitation",
#                         outpath=output_folder+"/tair_4co2_tac_ch0.png",
#                         var="precipitation_flux",
#                         cmap=my.Constants.colormaps.div_precip)

# for i in range(1,11):
#     try: d=eval("tac_4co2_change{}".format(i))
#     except: continue
#     title="4co2 tac change {} | Air Temperature".format(i)
#     out=output_folder+"/tair_4co2_tac_ch{}.png".format(i)
#     plt.figure()
#     anomalies(d,title=title,outpath=out)
#     plt.show()

#     title="4co2 tac change {} | Surface Temperature".format(i)
#     out=output_folder+"/tsurf_4co2_tac_ch{}.png".format(i)
#     plt.figure()
#     anomalies(d,title=title,outpath=out,var="surface_temperature")
#     plt.show()

#     title="4co2 tac change {} | Precipitation".format(i)
#     out=output_folder+"/precip_4co2_tac_ch{}.png".format(i)
#     plt.figure()
#     anomalies(d,title=title,outpath=out,var="precipitation_flux",
#               cmap=my.Constants.colormaps.div_precip)
#     plt.show()
