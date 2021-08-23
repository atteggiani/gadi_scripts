import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
import cProfile, pstats
import multiprocessing

outpath="/g/data3/w48/dm5220/data/figures"

ctl=my.open_mfdataset("/g/data/w48/dm5220/data/ctl/*_pa*.nc",
        parallel=True,concat_dim="time")
co2x4=my.open_mfdataset("/g/data/w48/dm5220/data/4co2/*_pa*.nc",
        parallel=True,concat_dim="time")
solar=my.open_mfdataset("/g/data/w48/dm5220/data/4co2_solar50-/*_pa*.nc",
        parallel=True,concat_dim="time")
sw=my.open_mfdataset("/g/data/w48/dm5220/data/4co2_sw_x0.9452_offset/*_pa*.nc",
        parallel=True,concat_dim="time")
sw_minus=my.open_mfdataset("/g/data/w48/dm5220/data/ctl_solar50+_sw-_x0.95/*_pa*.nc",
        parallel=True,concat_dim="time")        
sw_plus=my.open_mfdataset("/g/data/w48/dm5220/data/ctl_solar50-_sw+_x1.052/*_pa*.nc",
        parallel=True,concat_dim="time")

anomalies = lambda x,y,var: my.DataArray(x[var]-y[var])
all_data = [co2x4,solar,sw,sw_plus,sw_minus]
all_names = ["4co2","solar","sw","sw+_solar-","sw-_solar+"]

# SURFACE TEMP
# for data,name in zip(all_data,all_names):
for data,name in zip(all_data,all_names):
        print(f"Plotting Surface Temperature for {name}")
        anomalies(data,ctl,"surface_temperature").annual_mean(20*12).plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                units="K",
                title="Surface Temperature",
                outpath=os.path.join(outpath,f"{name}_tsurf_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Surface Temperature for {name}")
# PRECIP
for data,name in zip(all_data,all_names):
        print(f"Plotting Precipitation for {name}")
        anomalies(data,ctl,"precipitation_flux").to_mm_per_day().annual_mean(20*12).plotvar(
                cmap=my.Colormaps.div_precip,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Precipitation",
                units="mm/day",
                outpath=os.path.join(outpath,f"{name}_precip_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Precipitation for {name}")

# AIR TEMPERATURE
for data,name in zip(all_data,all_names):
        print(f"Plotting Air Temperature (longmean) for {name}")
        anomalies(data,ctl,"air_temperature").mean('longitude_0').annual_mean(20*12).plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (longitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{name}_tair_longmean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature for {name}")

for data,name in zip(all_data,all_names):
        print(f"Plotting Air Temperature (latmean) for {name}")
        anomalies(data,ctl,"air_temperature").latitude_mean().annual_mean(20*12).plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (latitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{name}_tair_latmean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature (latmean) for {name}")

# LW HEATING RATE
alpha=60*60*24
for data,name in zip(all_data,all_names):
        print(f"Plotting LW Heating Rate for {name}")
        (anomalies(data,ctl,"tendency_of_air_temperature_due_to_longwave_heating")*alpha).mean("longitude").annual_mean(20*12).plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate",
                outpath=os.path.join(outpath,f"{name}_LW_heating_rate.png"))
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate for {name}")

# SW HEATING RATE
alpha=60*60*24
for data,name in zip(all_data,all_names):
        print(f"Plotting SW Heating Rate for {name}")
        (anomalies(data,ctl,"tendency_of_air_temperature_due_to_shortwave_heating")*alpha).mean("longitude").annual_mean(20*12).plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate",
                outpath=os.path.join(outpath,f"{name}_SW_heating_rate.png"))
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate for {name}")

# SW Radiation (TOA out) 
for data,name in zip(all_data,all_names):
        print(f"Plotting SW Radiation (TOA) for {name}")
        anomalies(data,ctl,"toa_outgoing_shortwave_flux").annual_mean(20*12).plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-15,10,100),
                du=2.5,
                norm=colors.TwoSlopeNorm(vmin=-15,vcenter=0,vmax=10),
                title="SW Radiation TOA (Out)",
                units='$W\hspace{0.5}m^{-2}$',
                outpath=os.path.join(outpath,f"{name}_SW_out_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting SW Radiation (TOA) for {name}")

# LW Radiation (TOA out)
for data,name in zip(all_data,all_names):
        print(f"Plotting LW Radiation (TOA) for {name}")
        anomalies(data,ctl,"toa_outgoing_longwave_flux").annual_mean(20*12).plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-15,5,100),
                du=2.5,
                norm=colors.TwoSlopeNorm(vmin=-15,vcenter=0,vmax=5),
                title="LW Radiation TOA (Out)",
                units='$W\hspace{0.5}m^{-2}$',
                outpath=os.path.join(outpath,f"{name}_LW_out_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting LW Radiation (TOA) for {name}")
        
# VERTICAL PROFILES
# Air Temperature
print(f"Plotting Air Temperature vertical profiles")
fig=plt.figure()
for data,name in zip(all_data,all_names):
        anomalies(data,ctl,"air_temperature").annual_mean(20*12).global_mean().isel(pressure=slice(2,None)).plot(y="pressure",yincrease=False,yscale="log",label=f"{name}")
plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
plt.ylim([1000,50])
plt.gca().set_yticks([1000,800,600,400,200,50])
plt.gca().set_yticklabels(["{}".format(i) for i in [1000,800,600,400,200,50]])
plt.grid(ls="--",which='both')
plt.legend()
plt.xlabel("K")
plt.title("Air Temperature Vertical Profiles")
fig.savefig(os.path.join(outpath,"tair_vertical_profiles.png"),dpi=300)
plt.close()
collect()
print(f"Done plotting Air Temperature vertical profiles")

# SW Heating Rates
print(f"Plotting SW Heating Rates vertical profiles")
alpha=60*60*24
fig=plt.figure()
for data,name in zip(all_data,all_names):
        (anomalies(data,ctl,"tendency_of_air_temperature_due_to_shortwave_heating")*alpha).annual_mean(20*12).global_mean().isel(model_level_number=slice(None,32)).plot(y="model_level_number",label=f"{name}")
plt.vlines(0, 1, 32, colors='k', ls='--',lw=0.8)
plt.ylim([1,32])
arr=np.arange(1,32,5)
plt.gca().set_yticks(arr)
plt.gca().set_yticklabels(arr.tolist())
plt.grid(ls="--",which='both')
plt.legend()
plt.xlabel("K")
plt.ylabel("Model Level Number")
plt.title("SW Heating Rate Vertical Profiles")
fig.savefig(os.path.join(outpath,"sw_heating_rates_vertical_profiles.png"),dpi=300)
plt.close()
collect()
print(f"Done plotting SW Heating Rates vertical profiles")

# LW Heating Rates
print(f"Plotting LW Heating Rates vertical profiles")
alpha=60*60*24
fig=plt.figure()
for data,name in zip(all_data,all_names):
        (anomalies(data,ctl,"tendency_of_air_temperature_due_to_longwave_heating")*alpha).annual_mean(20*12).global_mean().isel(model_level_number=slice(None,32)).plot(y="model_level_number",label=f"{name}")
plt.vlines(0, 1, 32, colors='k', ls='--',lw=0.8)
plt.ylim([1,32])
arr=np.arange(1,32,5)
plt.gca().set_yticks(arr)
plt.gca().set_yticklabels(arr.tolist())
plt.grid(ls="--",which='both')
plt.legend()
plt.xlabel("K")
plt.ylabel("Model Level Number")
plt.title("LW Heating Rate Vertical Profiles")
fig.savefig(os.path.join(outpath,"lw_heating_rates_vertical_profiles.png"),dpi=300)
plt.close()
collect()
print(f"Done plotting SW Heating Rates vertical profiles")
print("Done!!!") 