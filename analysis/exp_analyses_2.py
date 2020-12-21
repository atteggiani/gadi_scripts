#%%
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

#DATA
data_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control/vabva_pa*.nc"),
                  concat_dim="time",parallel=True))
data_4co2 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2/vabvb_pa*.nc"),
                  concat_dim="time",parallel=True))
data_4co2_fix_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/vabvc_pa*.nc"),
                  concat_dim="time",parallel=True))
data_ctl_fix_ctl_solar_pl50 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_control_solar_plus50W/vabvp_pa*.nc"),
                  concat_dim="time",parallel=True))
data_4co2_solar_mi50 = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_solar_minus50W/vabvq_pa*.nc"),
                  concat_dim="time",parallel=True))



#%% SINGLE FIGURES
#( data , title , out_name )
datas_single=[
       (data_4co2, "4co2" , "4co2"),
       (data_4co2_fix_ctl , "4co2 + fixed control tsurf" , "4co2_Fctl"),
       (data_ctl_fix_ctl_solar_pl50 , "control + fixed control + solar +50 W/m2" , "ctl_Fctl_sol50p"),
       (data_4co2_solar_mi50 , "4co2 + solar -50 W/m2" , "4co2_sol50m")]

output_folder=input_folder+"/figures/amean"
exp_ = ["4co2","control + fixed 4co2 tsurf" , "control + fixed 4co2 SST" , "4co2 + fixed 4co2 tsurf + GREB",
        "control + solar +50 W/m2"]
for d,t,o in datas_single:
    m,mm = (-6,6) if t in exp_ else (-3,3)        
    #SURFACE TEMPERATURE
    var="surface_temperature"
    data=my.DataArray(d[var]-data_ctl[var]).annual_mean()
    p=my.DataArray(d[var]).t_student_probability(data_ctl[var])
    tit ="Surface temperature"
    outvar="tsurf"
    plt.figure()
    data.plotvar(
        levels=np.linspace(m,mm,100),
        cbar_kwargs={'ticks':np.arange(m,mm+1),'label':"°C"},
        title = "{} | {}".format(tit,t),
        t_student=p,
        outpath = os.path.join(output_folder,"{}_{}_amean.png".format(outvar,o)),
        cmap = my.Constants.colormaps.div_tsurf)
    plt.show()

    #AIR TEMPERATURE
    var="air_temperature"
    data=my.DataArray(d[var].mean('longitude_0')-data_ctl[var].mean('longitude_0')).annual_mean()
    p=my.DataArray(d[var].mean('longitude_0')).t_student_probability(data_ctl[var].mean('longitude_0'))
    tit ="Air temperature"
    outvar="tair"
    plt.figure()
    data.plotlev(
        levels=np.linspace(m,mm,100),
        cbar_kwargs={'ticks':np.arange(m,mm+1),'label':"°C"},
        title = "{} | {}".format(tit,t),
        t_student=p,
        outpath = os.path.join(output_folder,"{}_{}_amean.png".format(outvar,o)),
        cmap = my.Constants.colormaps.div_tsurf)
    plt.show()

    #PRECIPITATION
    var="precipitation_flux"
    data=my.DataArray(d[var]-data_ctl[var]).annual_mean()*alpha_precip
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




#%% DIFFERENCES
#( data , title , out_name )
datas_differences=[
       ((data_4co2_fix_ctl,data_ctl_fix_ctl_solar_pl50), "(4co2 fix) - (fix sol50+)" , "4co2fix_fixs50p"),
       ((data_4co2_fix_ctl,data_4co2_solar_mi50), "(4co2 fix) - (4co2 sol50-)" , "4co2fix_s50m"),
       ((data_4co2,data_4co2_fix_ctl), "(4co2) - (4co2 fix)" , "4co2_4co2fix"),
       ((data_4co2,data_ctl_fix_ctl_solar_pl50), "(4co2) - (fix sol50+)" , "4co2_fixs50p"),
       ((data_4co2,data_4co2_solar_mi50), "(4co2) - (4co2 sol50-)" , "4co2_s50m"),
       ]

output_folder_diff = output_folder=input_folder+"/figures/differences"

for d,t,o in datas_differences:
    #TSURF
    var="surface_temperature"
    data = my.DataArray(d[0][var]-d[1][var]).annual_mean()
    pvalue = my.DataArray(d[0][var]).t_student_probability(d[1][var])  
    plt.figure()
    data.plotvar(
            cmap = my.Constants.colormaps.div_tsurf,
            levels = np.linspace(-2,2,100),
            cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5),
                        "label":"°C"},
            t_student=pvalue,
            title = "Surface Temperature | {}".format(t),
            outpath = os.path.join(output_folder_diff,"diff_{}_tsurf.png".format(o)))
    plt.show()

    #TAIR
    var="air_temperature"
    data = my.DataArray(d[0][var].mean("longitude_0") - d[1][var].mean("longitude_0")).annual_mean()
    pvalue = my.DataArray(d[0][var].mean("longitude_0")).t_student_probability(d[1][var].mean("longitude_0"))
    plt.figure()
    data.plotlev(
            cmap = my.Constants.colormaps.div_tsurf,
            levels = np.linspace(-2,2,100),
            cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5),
                        "label":"°C"},
            t_student=pvalue,
            title = "Air Temperature | {}".format(t),
            outpath = os.path.join(output_folder_diff,"diff_{}_tair.png".format(o)))
    plt.show()

    #PRECIP
    var="precipitation_flux"
    data = my.DataArray(d[0][var]-d[1][var]).annual_mean()*alpha_precip
    pvalue = my.DataArray(d[0][var]).t_student_probability(d[1][var])  
    plt.figure()
    data.plotvar(
            cmap = my.Constants.colormaps.div_precip,
            levels = np.linspace(-2,2,100),
            cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5),
                        "label":"mm/day"},
            t_student=pvalue,
            title = "Precipitation | {}".format(t),
            outpath = os.path.join(output_folder_diff,"diff_{}_precip.png".format(o)))
    plt.show()



# %%
#VERTICAL PROFILES
#( data , title , out_name )
datas_profile=[
       (data_4co2, "4co2" , "4co2"),
       (data_4co2_fix_ctl , "4co2 + fix ctl " , "4co2_Fctl"),
       (data_ctl_fix_ctl_solar_pl50 , "fix ctl + solar 50+" , "ctl_Fctl_sol50p"),
       (data_4co2_solar_mi50 , "4co2 + solar 50-" , "4co2_sol50m")]

var="air_temperature"
output_folder_profiles = output_folder=input_folder+"/figures/various"

#GLOBAL
for d,t,o in datas_profile:
    old=my.DataArray(d[var]-data_ctl[var]).global_mean().annual_mean()
    new=xr.DataArray(data=old.pressure.values,dims=["pressure"],coords=[old.values],name="air_temperature")
    new.plot(
        yincrease=False,
        label="{}".format(t),
        yscale="log"
    )
plt.legend()
plt.yticks(ticks=[1000,800,600,400,200,50],labels=["1000","800","600","400","200","50"])
plt.ylim([1000,50])
plt.xlim([-8,5])
plt.title("Air Temperature | Vertical profiles")
plt.savefig(os.path.join(output_folder_profiles,"tair_profiles.png"), format = 'png', dpi = 300, bbox_inches = 'tight')
plt.show()

#TROPICS
for d,t,o in datas_profile:
    old=my.DataArray(d[var]-data_ctl[var]).sel(latitude_0=slice(-30,30)).global_mean().annual_mean()
    new=xr.DataArray(data=old.pressure.values,dims=["pressure"],coords=[old.values],name="air_temperature")
    new.plot(
        yincrease=False,
        label="{}".format(t),
        yscale="log"
    )
plt.legend()
plt.yticks(ticks=[1000,800,600,400,200,50],labels=["1000","800","600","400","200","50"])
plt.ylim([1000,50])
plt.xlim([-8,5])
plt.title("Air Temperature | Vertical profiles (Tropics)")
plt.savefig(os.path.join(output_folder_profiles,"tair_profiles_tropics.png"), format = 'png', dpi = 300, bbox_inches = 'tight')
plt.show()

# %%
