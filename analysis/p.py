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

ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control/vabva_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
fix=my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/vabvc_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))
tac_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test/vabua_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))           
tac_0_001 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_0.001/vabxa_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))         
tac_0_002 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_0.002/vabxb_pa*.nc"),
           concat_dim="time",parallel=True)).isel(time=slice(120,None))

datas=[(tac_ctl, "air temperature change - control" , "tac_ctl"),
       (fix, "4co2 + fixed control tsurf" , "4co2_Fctl"),
       (tac_0_001, "air temperature change - 0.001" , "tac_0.001"),
       (tac_0_002, "air temperature change - 0.002" , "tac_0.002")]

fun = lambda x,var: my.DataArray(x[var]).annual_mean()

def diff(data1,data2):
    data=fun(data1,"air_temperature_0").mean('longitude')-fun(data2,"air_temperature_0").mean('longitude')
    p=my.DataArray(data1["air_temperature_0"].mean('longitude')).t_student_probability(data2["air_temperature_0"].mean('longitude'))
    data.plotlev(
        levels=np.linspace(-3,3,100),
        cbar_kwargs={'ticks':np.arange(-3,3+1),'label':"°C"},
        title = "Air Temperature | Difference",
        t_student=p,
        cmap = my.Constants.colormaps.div_tsurf)

for d,t,o in datas:
    #SURFACE TEMPERATURE
    var="surface_temperature"
    data=fun(d,var)-fun(ctl,var)
    p=my.DataArray(d[var]).t_student_probability(ctl[var])
    tit ="Surface temperature"
    outvar="tsurf"
    plt.figure()
    data.plotvar(
        levels=np.linspace(-3,3,100),
        cbar_kwargs={'ticks':np.arange(-3,3+1),'label':"°C"},
        title = "{} | {}".format(tit,t),
        t_student=p,
        outpath = os.path.join(output_folder,"{}_{}_amean.png".format(outvar,o)),
        cmap = my.Constants.colormaps.div_tsurf)
    plt.show()

    #AIR TEMPERATURE
    var="air_temperature"
    data=fun(d,var).mean('longitude_0')-fun(ctl,var).mean('longitude_0')
    p=my.DataArray(d[var].mean('longitude_0')).t_student_probability(ctl[var].mean('longitude_0'))
    tit ="Air temperature"
    outvar="tair"
    plt.figure()
    data.plotlev(
        levels=np.linspace(-3,3,100),
        cbar_kwargs={'ticks':np.arange(-3,3+1),'label':"°C"},
        title = "{} | {}".format(tit,t),
        t_student=p,
        outpath = os.path.join(output_folder,"{}_{}_amean.png".format(outvar,o)),
        cmap = my.Constants.colormaps.div_tsurf)
    plt.show()

    #AIR TEMPERATURE in Model levels
    var="air_temperature_0"
    data=fun(d,var).mean('longitude')-fun(ctl,var).mean('longitude')
    p=my.DataArray(d[var].mean('longitude')).t_student_probability(ctl[var].mean('longitude'))
    tit ="Air temperature"
    outvar="tair_0"
    plt.figure()
    data.plotlev(
        levels=np.linspace(-3,3,100),
        cbar_kwargs={'ticks':np.arange(-3,3+1),'label':"°C"},
        title = "{} | {}".format(tit,t),
        t_student=p,
        outpath = os.path.join(output_folder,"{}_{}_amean.png".format(outvar,o)),
        cmap = my.Constants.colormaps.div_tsurf)
    plt.show()

    #PRECIPITATION
    var="precipitation_flux"
    data=(fun(d,var)-fun(ctl,var))*alpha_precip
    p=my.DataArray(d[var]).t_student_probability(ctl[var])
    tit ="Precipitation"
    outvar="precip"
    plt.figure()
    data.plotvar(
        a=alpha_precip,
        levels=np.linspace(-2,2,100),
        cbar_kwargs={'ticks':np.arange(-2,2+0.5,0.5),'label':"mm/day"},
        title = "{} | {}".format(tit,t),
        t_student=p,
        outpath = os.path.join(output_folder,"{}_{}_amean.png".format(outvar,o)),
        cmap = my.Constants.colormaps.div_precip)
    plt.show()
