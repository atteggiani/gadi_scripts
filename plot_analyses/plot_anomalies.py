import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
from argparse import ArgumentParser

# SURFACE TEMP
def plot_tsurf(data,outname,func=lambda x: x):   
        var="surface_temperature"     
        print(f"Plotting Surface Temperature for {outname}")
        P=p(data,var)
        data = func(anomalies(data,var))
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=levels1,
                du=du1,
                units=units['K'],
                title="Surface Temperature",
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tsurf_amean{norm}.png"))
        plt.clf()
        collect()
        print(f"Done plotting Surface Temperature for {outname}")

# PRECIP
def plot_precip(data,outname,func=lambda x: x):   
        var="precipitation_flux"     
        print(f"Plotting Precipitation for {outname}")
        P=p(data,var)
        data = func(anomalies(data,var))
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotvar(
                cmap=my.Colormaps.div_precip,
                levels=levels1,
                du=du1,
                title="Precipitation",
                units=units['mm/day'],
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_precip_amean{norm}.png"))
        plt.clf()
        collect()
        print(f"Done plotting Precipitation for {outname}")

# AIR TEMPERATURE
def plot_tair_longmean_plev(data,outname,func=lambda x: x):
        var = "air_temperature_0_plev"
        if var not in data: return
        print(f"Plotting Air Temperature (longmean) for {outname} on pressure levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=levels1,
                du=du1,
                title="Air Temperature (longitude mean)",
                units=units['K'],
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_longmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_longmean_mlev(data,outname,func=lambda x: x):
        var = "air_temperature_0"
        if var not in data: return
        print(f"Plotting Air Temperature (longmean) for {outname} on model levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=levels1,
                du=du1,
                title="Air Temperature (longitude mean)",
                units=units['K'],
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_longmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_latmean_plev(data,outname,func=lambda x: x):
        var = "air_temperature_0_plev"
        if var not in data: return
        print(f"Plotting Air Temperature (latmean) for {outname} on pressure levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=levels1,
                du=du1,
                title="Air Temperature (latitude mean)",
                units=units['K'],
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_latmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_latmean_mlev(data,outname,func=lambda x: x):
        var = "air_temperature_0"
        if var not in data: return
        print(f"Plotting Air Temperature (latmean) for {outname} on model levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=levels1,
                du=du1,
                title="Air Temperature (latitude mean)",
                units=units['K'],
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_latmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

# LW HEATING RATE
def plot_lw_hrate_longmean_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if var not in data: return
        print(f"Plotting LW Heating Rate (longmean) for {outname} on pressure levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="LW Heating Rate (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_longmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_lw_hrate_longmean_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_longwave_heating"
        if var not in data: return
        print(f"Plotting LW Heating Rate (longmean) for {outname} on model levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="LW Heating Rate (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_longmean_mlev{norm}.png")
                )
        plt.clf()
        collect()        

def plot_lw_hrate_latmean_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if var not in data: return 
        print(f"Plotting LW Heating Rate (latmean) for {outname} on pressure levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="LW Heating Rate (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_latmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_lw_hrate_latmean_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_longwave_heating"
        if var not in data: return 
        print(f"Plotting LW Heating Rate (latmean) for {outname} on model levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="LW Heating Rate (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_latmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

# SW HEATING RATE
def plot_sw_hrate_longmean_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (longmean) for {outname} on pressure levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="SW Heating Rate (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_longmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_sw_hrate_longmean_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_shortwave_heating"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (longmean) for {outname} on model levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="SW Heating Rate (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_longmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

def plot_sw_hrate_latmean_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (latmean) for {outname} on pressure levels") 
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="SW Heating Rate (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_latmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_sw_hrate_latmean_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_shortwave_heating"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (latmean) for {outname} on model levels") 
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="SW Heating Rate (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_latmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

# TOT HEATING RATE
def plot_tot_hrate_longmean_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_total_heating_plev"
        if (var not in data): return
        print(f"Plotting TOT Heating Rate (longmean) for {outname} on pressure levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="TOT Heating Rate (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_longmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tot_hrate_longmean_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_total_heating_plev"
        if (var not in data): return
        print(f"Plotting TOT Heating Rate (longmean) for {outname} on model levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="TOT Heating Rate (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_longmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tot_hrate_latmean_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_total_heating_plev"
        if (var not in data): return
        print(f"Plotting TOT Heating Rate (latmean) for {outname} on pressure levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="TOT Heating Rate (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_latmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tot_hrate_latmean_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_total_heating_plev"
        if (var not in data): return
        print(f"Plotting TOT Heating Rate (latmean) for {outname} on model levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels2,
                cmap=my.Colormaps.div_tsurf,
                du=du2,
                units=units['K/day'],
                title="TOT Heating Rate (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_latmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

# TAIR CHANGE DUE TO LS PRECIP
def plot_tair_change_ls_longmean_plev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_stratiform_precipitation_plev"
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to LS Precipitation (longmean) for {outname} on pressure levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to LS Precip (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_ls_longmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_ls_longmean_mlev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_stratiform_precipitation"
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to LS Precipitation (longmean) for {outname} on model levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to LS Precip (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_ls_longmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_ls_latmean_plev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_stratiform_precipitation_plev"
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to LS Precipitation (latmean) for {outname} on pressure levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to LS Precip (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_ls_latmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_ls_latmean_mlev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_stratiform_precipitation"
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to LS Precipitation (latmean) for {outname} on model levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to LS Precip (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_ls_latmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

# TAIR CHANGE DUE TO CONVECTION
def plot_tair_change_conv_longmean_plev(data,outname,func=lambda x: x):
        var='change_over_time_in_air_temperature_due_to_convection_plev'
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to Convection (longmean) for {outname} on pressure levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to Convection (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_conv_longmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_conv_longmean_mlev(data,outname,func=lambda x: x):
        var='change_over_time_in_air_temperature_due_to_convection_plev'
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to Convection (longmean) for {outname} on model levels")
        P=p(data,var).longitude_mean()
        data = func(anomalies(data,var))
        data = data.longitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to Convection (longitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_conv_longmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_conv_latmean_plev(data,outname,func=lambda x: x):
        var='change_over_time_in_air_temperature_due_to_convection_plev'
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to Convection (latmean) for {outname} on pressure levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to Convection (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_conv_latmean_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_conv_latmean_mlev(data,outname,func=lambda x: x):
        var='change_over_time_in_air_temperature_due_to_convection_plev'
        if var not in data: return 
        print(f"Plotting Air Temperature Change due to Convection (latmean) for {outname} on model levels")
        P=p(data,var).latitude_mean()
        data = func(anomalies(data,var))
        data = data.latitude_mean()
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotlev(
                levels=levels3,
                cmap=my.Colormaps.div_tsurf,
                du=du3,
                units=units['K'],
                title="Tair Change due to Convection (latitude mean)",
                double_axis=True,
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_tair_change_conv_latmean_mlev{norm}.png")
                )
        plt.clf()
        collect()

# SW RADATION (TOA OUT)
def plot_sw_out(data,outname,func=lambda x: x):
        var='toa_outgoing_shortwave_flux'
        if var not in data: return 
        print(f"Plotting SW Radiation out (TOA) for {outname}")
        if normalize:
            levels=np.linspace(-1,1,50)
            du=0.25
        else:
            levels=np.linspace(-15,10,50)
            du=2.5
        P=p(data,var)
        data = func(anomalies(data,var))
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=levels,
                du=du,
                norm=colors.TwoSlopeNorm(vmin=-15,vcenter=0,vmax=10),
                title="SW Radiation TOA (Out)",
                units='$W\hspace{0.5}m^{-2}$',
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_SW_out_amean{norm}.png"))
        plt.clf()
        collect()
        print(f"Done plotting SW Radiation out (TOA) for {outname}")

# LW RADATION (TOA OUT)
def plot_lw_out(data,outname,func=lambda x: x):
        var="toa_outgoing_longwave_flux"
        if var not in data: return 
        print(f"Plotting LW Radiation out (TOA) for {outname}")
        if normalize:
            levels=np.linspace(-1,1,50)
            du=0.25
        else:
            levels=np.linspace(-15,5,50)
            du=2.5
        P=p(data,var)
        data = func(anomalies(data,var))
        data = data.annual_mean(nyears*12,normalize=normalize)
        data.plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=levels,
                du=du,
                norm=colors.TwoSlopeNorm(vmin=-15,vcenter=0,vmax=5),
                title="LW Radiation TOA (Out)",
                units='$W\hspace{0.5}m^{-2}$',
                t_student=P,
                outpath=os.path.join(outpath,f"{outname}_LW_out_amean{norm}.png"))
        plt.clf()
        collect()
        print(f"Done plotting LW Radiation out (TOA) for {outname}")

# AIR TEMPERATURE VERTPROF
def plot_tair_vert_plev(data,outname,func=lambda x: x):
        var = "air_temperature_0_plev"
        if var not in data: return
        print(f"Plotting Air Temperature vertical profile for {outname} on pressure levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-4,6)
            dx=1
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="Air Temperature",
                outpath=os.path.join(outpath,f"{outname}_tair_vert_plev{norm}.png"))
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature vertical profile for {outname} on pressure levels")

def plot_tair_vert_mlev(data,outname,func=lambda x: x):
        var = "air_temperature_0"
        if var not in data: return
        print(f"Plotting Air Temperature vertical profile for {outname} on model levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-4,6)
            dx=1
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="Air Temperature",
                outpath=os.path.join(outpath,f"{outname}_tair_vert_mlev{norm}.png"))
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature vertical profile for {outname} on model levels")

# LW HEATING RATE VERTPROF
def plot_lw_hrate_vert_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if var not in data: return
        print(f"Plotting LW Heating Rate vertical profile for {outname} on pressure levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.3,0.3)
            dx=0.1
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K/day',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="LW Heating Rate",
                outpath=os.path.join(outpath,f"{outname}_lw_hrate_vert_plev{norm}.png")
                )
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate vertical profile for {outname} on pressure levels")

def plot_lw_hrate_vert_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_longwave_heating"
        if var not in data: return
        print(f"Plotting LW Heating Rate vertical profile for {outname} on model levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.3,0.3)
            dx=0.1
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K/day',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="LW Heating Rate",
                outpath=os.path.join(outpath,f"{outname}_lw_hrate_vert_mlev{norm}.png")
                )
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate vertical profile for {outname} on model levels")

# SW HEATING RATE VERTPROF
def plot_sw_hrate_vert_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        if var not in data: return
        print(f"Plotting SW Heating Rate vertical profile for {outname} on pressure levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.15,0.15)
            dx=0.05
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K/day',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="SW Heating Rate",
                outpath=os.path.join(outpath,f"{outname}_sw_hrate_vert_plev{norm}.png")
                )
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate vertical profile for {outname} on pressure levels")

def plot_sw_hrate_vert_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_shortwave_heating"
        if var not in data: return
        print(f"Plotting SW Heating Rate vertical profile for {outname} on model levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.15,0.15)
            dx=0.05
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K/day',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="SW Heating Rate",
                outpath=os.path.join(outpath,f"{outname}_sw_hrate_vert_mlev{norm}.png")
                )
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate vertical profile for {outname} on model levels")

# TOT HEATING RATE VERTPROF
def plot_tot_hrate_vert_plev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_total_heating_plev"
        if var not in data: return
        print(f"Plotting TOT Heating Rate vertical profile for {outname} on pressure levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.3,0.3)
            dx=0.1
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K/day',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="TOT Heating Rate",
                outpath=os.path.join(outpath,f"{outname}_tot_hrate_vert_plev{norm}.png")
                )
        plt.clf()
        collect()
        print(f"Done plotting TOT Heating Rate vertical profile for {outname} on pressure levels")

def plot_tot_hrate_vert_mlev(data,outname,func=lambda x: x):
        var = "tendency_of_air_temperature_due_to_total_heating_plev"
        if var not in data: return
        print(f"Plotting TOT Heating Rate vertical profile for {outname} on model levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.3,0.3)
            dx=0.1
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K/day',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="TOT Heating Rate",
                outpath=os.path.join(outpath,f"{outname}_tot_hrate_vert_mlev{norm}.png")
                )
        plt.clf()
        collect()
        print(f"Done plotting TOT Heating Rate vertical profile for {outname} on model levels")

# TAIR CHANGE DUE TO LS PRECIP VERTPROF
def plot_tair_change_ls_vert_plev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_stratiform_precipitation_plev"
        if var not in data: return
        print(f"Plotting Air Temperature Change due to LS Precip vertical profile for {outname} on pressure levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.002,0.002)
            dx=0.0005
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="Tair Change due to LS Precip",
                outpath=os.path.join(outpath,f"{outname}_tair_change_ls_vert_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_ls_vert_mlev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_stratiform_precipitation"
        if var not in data: return
        print(f"Plotting Air Temperature Change due to LS Precip vertical profile for {outname} on model levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.002,0.002)
            dx=0.0005
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="Tair Change due to LS Precip",
                outpath=os.path.join(outpath,f"{outname}_tair_change_ls_vert_mlev{norm}.png")
                )
        plt.clf()
        collect()

# TAIR CHANGE DUE TO CONVECTION VERTPROF
def plot_tair_change_conv_vert_plev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_convection_plev"
        if var not in data: return
        print(f"Plotting Air Temperature Change due to Convection vertical profile for {outname} on pressure levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.002,0.002)
            dx=0.0005
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="Tair Change due to Convection",
                outpath=os.path.join(outpath,f"{outname}_tair_change_conv_vert_plev{norm}.png")
                )
        plt.clf()
        collect()

def plot_tair_change_conv_vert_mlev(data,outname,func=lambda x: x):
        var = "change_over_time_in_air_temperature_due_to_convection"
        if var not in data: return
        print(f"Plotting Air Temperature Change due to Convection vertical profile for {outname} on model levels")
        if normalize:
            xlim=(-1,1)
            dx=0.25
        else:
            xlim=(-0.002,0.002)
            dx=0.0005
        data = func(anomalies(data,var))
        data = data.global_mean()
        data.plotprof(
                timesteps=nyears*12,
                labels = outname,
                units = 'K',
                double_axis=True,
                xlim=xlim,
                dx=dx,
                title="Tair Change due to Convection",
                outpath=os.path.join(outpath,f"{outname}_tair_change_conv_vert_mlev{norm}.png")
                )
        plt.clf()
        collect()


def all_plots(data,outname):
        plot_tsurf(data,outname)
        plot_precip(data,outname,func=lambda x: x.to_mm_per_day())
        plot_tair_longmean_plev(data,outname)
        plot_tair_longmean_mlev(data,outname)
        plot_tair_latmean_plev(data,outname)
        plot_tair_latmean_mlev(data,outname)
        plot_lw_hrate_longmean_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_lw_hrate_longmean_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_lw_hrate_latmean_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_lw_hrate_latmean_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_sw_hrate_longmean_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_sw_hrate_longmean_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_sw_hrate_latmean_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_sw_hrate_latmean_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tot_hrate_longmean_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tot_hrate_longmean_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tot_hrate_latmean_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tot_hrate_latmean_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tair_change_ls_longmean_plev(data,outname)
        plot_tair_change_ls_longmean_mlev(data,outname)
        plot_tair_change_ls_latmean_plev(data,outname)
        plot_tair_change_ls_latmean_mlev(data,outname)
        plot_tair_change_conv_longmean_plev(data,outname)
        plot_tair_change_conv_longmean_mlev(data,outname)
        plot_tair_change_conv_latmean_plev(data,outname)
        plot_tair_change_conv_latmean_mlev(data,outname)
        plot_lw_out(data,outname)
        plot_sw_out(data,outname)
        plot_tair_vert_plev(data,outname)
        plot_tair_vert_mlev(data,outname)
        plot_lw_hrate_vert_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_lw_hrate_vert_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_sw_hrate_vert_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_sw_hrate_vert_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tot_hrate_vert_plev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tot_hrate_vert_mlev(data,outname,func=lambda x: x.to_K_per_day(force=True))
        plot_tair_change_ls_vert_plev(data,outname)
        plot_tair_change_ls_vert_mlev(data,outname)
        plot_tair_change_conv_vert_plev(data,outname)
        plot_tair_change_conv_vert_mlev(data,outname)

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,nargs='*')
parser.add_argument('-o','--outnames',type=str,nargs='*')
parser.add_argument('-C','--control',type=str,default="ctl")
parser.add_argument('-n','--normalize',action="store_true")
parser.add_argument('-t','--t_student',action="store_false")
parser.add_argument('-d','--directory',type=str,default="/g/data3/w40/dm5220/data/figures/anomalies")
args=parser.parse_args()

files=args.input
outnames=args.outnames
control_file=args.control
normalize=args.normalize
t_student=args.t_student
outpath=args.directory
os.makedirs(outpath,exist_ok=True)

units={'K':'$K$',
       'mm/day':'$(mm \cdot d^{-1})$',
       'K/day':'$(K \cdot d^{-1})$'}

if normalize:
    norm="_norm"
    levels1=levels2=levels3=np.linspace(-1,1,50)
    du1=du2=du3=0.25 
    units={i:f"{j[:-1]}/{j[1:]}" for i,j in units.items()}
else:
    norm=""
    levels1=np.linspace(-2,2,50)
    levels2=np.linspace(-0.1,0.1,50)
    levels3=np.linspace(-0.001,0.001,50)
    du1=0.5
    du2=0.02
    du3=0.0002

if outnames is None:
        outnames = files
if len(files) != len(outnames):
        raise Exception(f"Number of input files and output names mismatch. \
Number of input files is {len(files)}. \
Number of output names is {len(outnames)}")
nyears=20
ctl = my.UM.read_data(control_file)
anomalies = lambda x,var: my.DataArray(x[var]-ctl[var])
p = lambda x,var: x[var].t_student_probability(ctl[var],num_years=nyears)

for file,outname in zip(files,outnames):
        print(f"Reading {file}...")
        data = my.UM.read_data(file)
        all_plots(data,outname)
plt.close()