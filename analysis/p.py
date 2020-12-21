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
           concat_dim="time",parallel=True))
fix=my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/vabvc_pa*.nc"),
           concat_dim="time",parallel=True))  
tac_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test/vabua_pa*.nc"),
           concat_dim="time",parallel=True))           
tac_0_01 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_0.01/vabxc_pa*.nc"),
           concat_dim="time",parallel=True))           
tac_0_02 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test_0.02/vabxa_pa*.nc"),
           concat_dim="time",parallel=True))                      

datas=[(tac_ctl, "air temperature change - control" , "tac_ctl"),
       (fix , "4co2 + fixed control tsurf" , "4co2_Fctl"),
       (tac_0_01, "air temperature change - 0.01" , "tac_0.01"),
       (tac_0_02, "air temperature change - 0.02" , "tac_0.02")]

for d,t,o in datas:
    print(t)

data_ctl=ctl.isel(time=slice(0,120))
fun = lambda x,var: my.DataArray(x[var]).annual_mean()

for d,t,o in datas:
    #SURFACE TEMPERATURE
    var="surface_temperature"
    data=fun(d,var)-fun(data_ctl,var)
    p=my.DataArray(d[var]).t_student_probability(data_ctl[var])
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
    data=fun(d,var).mean('longitude_0')-fun(data_ctl,var).mean('longitude_0')
    p=my.DataArray(d[var].mean('longitude_0')).t_student_probability(data_ctl[var].mean('longitude_0'))
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
    data=fun(d,var).mean('longitude')-fun(data_ctl,var).mean('longitude')
    p=my.DataArray(d[var].mean('longitude')).t_student_probability(data_ctl[var].mean('longitude'))
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
    data=(fun(d,var)-fun(data_ctl,var))*alpha_precip
    p=my.DataArray(d[var]).t_student_probability(data_ctl[var])
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
