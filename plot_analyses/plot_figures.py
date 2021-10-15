'''
Same as "plot_nomalies.py" but with default data
'''
import myfuncs as my
import xarray as xr
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
import concurrent.futures
import dask
from dask.diagnostics import ProgressBar
from decorators import timed

def read_data(input_folder,files):
        data=[]
        for file in files:
            data.append(my.open_mfdataset(
                os.path.join(
                        input_folder,
                        f"{file}/*_pa*.nc"),
                parallel=True,
                combine="nested",
                concat_dim="time",
                compat='override',
                coords='minimal',
                ))
        return data

def read_data_parallel(input_folder,files):
        def _read(input_folder,file):
                data = my.open_mfdataset(
                        os.path.join(
                                input_folder,
                                f"{file}/*_pa*.nc"),
                        combine="nested",
                        concat_dim="time",
                        compat='override',
                        coords='minimal',
                        )
                return data
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
                data = executor.map(lambda x: _read(input_folder,x),files)               
        return list(data)

# SURFACE TEMP
def plot_tsurf(data,data_ctl,outname):        
        print(f"Plotting Surface Temperature for {outname}")
        data=anomalies(data,data_ctl,"surface_temperature")
        data = data.annual_mean(20*12)
        data.plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                units="K",
                title="Surface Temperature",
                outpath=os.path.join(outpath,f"{outname}_tsurf_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Surface Temperature for {outname}")

# PRECIP
def plot_precip(data,data_ctl,outname):        
        print(f"Plotting Precipitation for {outname}")
        data=anomalies(data,data_ctl,"precipitation_flux")
        data=data.to_mm_per_day()
        data = data.annual_mean(20*12)
        data.plotvar(
                cmap=my.Colormaps.div_precip,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Precipitation",
                units="mm/day",
                outpath=os.path.join(outpath,f"{outname}_precip_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Precipitation for {outname}")

# AIR TEMPERATURE
def plot_tair_longmean(data,data_ctl,outname):
        print(f"Plotting Air Temperature (longmean) for {outname}")
        if "air_temperature_0_plev" in data:
                var = "air_temperature_0_plev"
        else:
                var = "air_temperature"
        data = anomalies(data,data_ctl,var)
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (longitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{outname}_tair_longmean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature (longmean) for {outname}")

def plot_tair_latmean(data,data_ctl,outname):
        print(f"Plotting Air Temperature (latmean) for {outname}")
        if "air_temperature_0_plev" in data:
                var = "air_temperature_0_plev"
        else:
                var = "air_temperature"
        data = anomalies(data,data_ctl,var)
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (latitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{outname}_tair_latmean.png"))
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature (latmean) for {outname}")

# LW HEATING RATE
def plot_lw_hrate_longmean(data,data_ctl,outname):
        print(f"Plotting LW Heating Rate (longmean) for {outname}")
        if "tendency_of_air_temperature_due_to_longwave_heating_plev" in data:
                var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        else:
                var = "tendency_of_air_temperature_due_to_longwave_heating"   
        data = anomalies(data,data_ctl,var)
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_longmean.png"))
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate (longmean) for {outname}")

def plot_lw_hrate_latmean(data,data_ctl,outname):
        print(f"Plotting LW Heating Rate (latmean) for {outname}")
        if "tendency_of_air_temperature_due_to_longwave_heating_plev" in data:
                var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        else:
                var = "tendency_of_air_temperature_due_to_longwave_heating"   
        data = anomalies(data,data_ctl,var)
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate (latitude mean)",
                )
        plt.xlim([-0.3,0.2])
        plt.savefig(os.path.join(outpath,f"{outname}_LW_hrate_latmean.png"),
                    dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate (longmean) for {outname}")

# SW HEATING RATE
def plot_sw_hrate_longmean(data,data_ctl,outname):
        print(f"Plotting SW Heating Rate (longmean) for {outname}")
        if "tendency_of_air_temperature_due_to_longwave_heating_plev" in data:
                var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        else:
                var = "tendency_of_air_temperature_due_to_shortwave_heating"   
        data = anomalies(data,data_ctl,var)
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (longitude mean)",
                )
        plt.xlim([-0.3,0.2])
        plt.savefig(os.path.join(outpath,f"{outname}_SW_hrate_latmean.png"),
                    dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate (longmean) for {outname}")

def plot_sw_hrate_latmean(data,data_ctl,outname):
        print(f"Plotting SW Heating Rate (latmean) for {outname}")
        if "tendency_of_air_temperature_due_to_longwave_heating_plev" in data:
                var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        else:
                var = "tendency_of_air_temperature_due_to_shortwave_heating"   
        data = anomalies(data,data_ctl,var)
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_latmean.png"))
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate (longmean) for {outname}")

# SW Radiation (TOA out) 
def plot_sw_out(data,data_ctl,outname):
        print(f"Plotting SW Radiation out (TOA) for {outname}")
        data = anomalies(data,data_ctl,"toa_outgoing_shortwave_flux")
        data = data.annual_mean(20*12)
        data.plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-15,10,100),
                du=2.5,
                norm=colors.TwoSlopeNorm(vmin=-15,vcenter=0,vmax=10),
                title="SW Radiation TOA (Out)",
                units='$W\hspace{0.5}m^{-2}$',
                outpath=os.path.join(outpath,f"{outname}_SW_out_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting SW Radiation out (TOA) for {outname}")

# LW Radiation (TOA out) 
def plot_lw_out(data,data_ctl,outname):
        print(f"Plotting LW Radiation out (TOA) for {outname}")
        data = anomalies(data,data_ctl,"toa_outgoing_longwave_flux")
        data = data.annual_mean(20*12)
        data.plotvar(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-15,5,100),
                du=2.5,
                norm=colors.TwoSlopeNorm(vmin=-15,vcenter=0,vmax=5),
                title="LW Radiation TOA (Out)",
                units='$W\hspace{0.5}m^{-2}$',
                outpath=os.path.join(outpath,f"{outname}_LW_out_amean.png"))
        plt.clf()
        collect()
        print(f"Done plotting LW Radiation out (TOA) for {outname}")

# VERTICAL PROFILES
# Air Temperature
def plot_tair_vertical(all_data,outnames):
        print(f"Plotting Air Temperature vertical profiles")
        cond=["air_temperature_0_plev" in data for data in all_data] 
        if np.all(cond):
                var = "air_temperature_0_plev"
        else:
                var = "air_temperature"
        for data,outname in zip(all_data,outnames):
                data = anomalies(data,ctl,var)
                data = data.sel(pressure=slice(49,1001))
                data = data.annual_mean(20*12)
                data = data.global_mean()
                data.plot(
                        y="pressure",
                        yincrease=False,
                        yscale="log",
                        label=f"{outname}")
        plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        plt.ylim([1000,50])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(["{}".format(i) for i in [1000,800,600,400,200,50]])
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K")
        plt.title("Air Temperature Vertical Profiles")
        plt.savefig(os.path.join(outpath,"tair_vertical_profiles.png"),dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature vertical profiles")

# SW Heating Rates
def plot_sw_hrate_vertical(all_data,outnames):
        print(f"Plotting SW Heating Rate vertical profiles")
        cond=["tendency_of_air_temperature_due_to_shortwave_heating_plev" in data for data in all_data] 
        if np.all(cond):
                var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
                selection =lambda x: x.sel(pressure=slice(49,1001))
                y="pressure"
                vline=lambda x: x.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
                ylim=[1000,50]
                yticks=np.array([1000,800,600,400,200,50])
                ylabel="pressure [hPa]"
                yscale="log"
                yincrease=False
        else:
                var = "tendency_of_air_temperature_due_to_shortwave_heating"
                selection =lambda x: x.sel(model_level_number=slice(-0.5,32.5))
                y="model_level_number"
                vline=lambda x: x.vlines(0, 1, 32, colors='k', ls='--',lw=0.8)
                ylim=[1,32]
                yticks=np.arange(1,32,5)
                ylabel="Model Level Number"
                yscale="linear"
                yincrease=True

        for data,outname in zip(all_data,outnames):
                data = anomalies(data,ctl,var)
                data = selection(data)
                data = data*60*60*24
                data = data.annual_mean(20*12)
                data = data.global_mean()
                data.plot(
                        y=y,
                        yincrease=yincrease,
                        yscale=yscale,
                        label=f"{outname}")
        vline(plt)
        plt.ylim(ylim)
        plt.xlim([-0.3,0.2])
        plt.gca().set_yticks(yticks)
        plt.gca().set_yticklabels(yticks.tolist())
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel(ylabel)
        plt.title("SW Heating Rate Vertical Profiles")
        plt.savefig(os.path.join(outpath,"sw_hrate_vertical_profiles.png"),dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate vertical profiles")

# LW Heating Rates
def plot_lw_hrate_vertical(all_data,outnames):
        print(f"Plotting LW Heating Rate vertical profiles")
        cond=["tendency_of_air_temperature_due_to_longwave_heating_plev" in data for data in all_data] 
        if np.all(cond):
                var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
                selection =lambda x: x.sel(pressure=slice(49,1001))
                y="pressure"
                vline=lambda x: x.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
                ylim=[1000,50]
                yticks=np.array([1000,800,600,400,200,50])
                ylabel="pressure [hPa]"
                yscale="log"
                yincrease=False
        else:
                var = "tendency_of_air_temperature_due_to_longwave_heating"
                selection =lambda x: x.sel(model_level_number=slice(-0.5,32.5))
                y="model_level_number"
                vline=lambda x: x.vlines(0, 1, 32, colors='k', ls='--',lw=0.8)
                ylim=[1,32]
                yticks=np.arange(1,32,5)
                ylabel="Model Level Number"
                yscale="linear"
                yincrease=True

        for data,outname in zip(all_data,outnames):
                data = anomalies(data,ctl,var)
                data = selection(data)
                data = data*60*60*24
                data = data.annual_mean(20*12)
                data = data.global_mean()
                data.plot(
                        y=y,
                        yincrease=yincrease,
                        yscale=yscale,
                        label=f"{outname}")
        vline(plt)
        plt.ylim(ylim)
        plt.xlim([-0.3,0.2])
        plt.gca().set_yticks(yticks)
        plt.gca().set_yticklabels(yticks.tolist())
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel(ylabel)
        plt.title("LW Heating Rate Vertical Profiles")
        plt.savefig(os.path.join(outpath,"lw_hrate_vertical_profiles.png"),dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate vertical profiles")

# TOT Heating Rates (SW+LW)
def plot_tot_hrate_vertical(all_data,outnames):
        print(f"Plotting TOT Heating Rate vertical profiles")
        cond=[("tendency_of_air_temperature_due_to_longwave_heating_plev" in data) and
              ("tendency_of_air_temperature_due_to_shortwave_heating_plev" in data) 
              for data in all_data] 
        if np.all(cond):
                var1 = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
                var2 = "tendency_of_air_temperature_due_to_longwave_heating_plev"
                selection =lambda x: x.sel(pressure=slice(49,1001))
                y="pressure"
                vline=lambda x: x.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
                ylim=[1000,50]
                yticks=np.array([1000,800,600,400,200,50])
                ylabel="pressure [hPa]"
                yscale="log"
                yincrease=False
        else:
                var1 = "tendency_of_air_temperature_due_to_shortwave_heating"
                var2 = "tendency_of_air_temperature_due_to_longwave_heating"
                selection =lambda x: x.sel(model_level_number=slice(-0.5,32.5))
                y="model_level_number"
                vline=lambda x: x.vlines(0, 1, 32, colors='k', ls='--',lw=0.8)
                ylim=[1,32]
                yticks=np.arange(1,32,5)
                ylabel="Model Level Number"
                yscale="linear"
                yincrease=True

        for data,outname in zip(all_data,outnames):
                data1 = anomalies(data,ctl,var1)
                data2 = anomalies(data,ctl,var2)
                data = data1+data2
                data = selection(data)
                data = data*60*60*24
                data = data.annual_mean(20*12)
                data = data.global_mean()
                data.plot(
                        y=y,
                        yincrease=yincrease,
                        yscale=yscale,
                        label=f"{outname}")
        vline(plt)
        plt.ylim(ylim)
        plt.xlim([-0.3,0.2])
        plt.gca().set_yticks(yticks)
        plt.gca().set_yticklabels(yticks.tolist())
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel(ylabel)
        plt.title("Total (SW + LW) Heating Rate Vertical Profiles")
        plt.savefig(os.path.join(outpath,"tot_hrate_vertical_profiles.png"),dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting TOT Heating Rate vertical profiles")

def all_plots():        
        for data,outname in zip(all_data,outnames):
                plot_tsurf(data,ctl,outname)
                plot_precip(data,ctl,outname)
                plot_tair_longmean(data,ctl,outname)
                plot_tair_latmean(data,ctl,outname)
                plot_lw_hrate_longmean(data,ctl,outname)
                plot_lw_hrate_latmean(data,ctl,outname)
                plot_sw_hrate_longmean(data,ctl,outname)
                plot_sw_hrate_latmean(data,ctl,outname)
                plot_lw_out(data,ctl,outname)
                plot_sw_out(data,ctl,outname)
        plot_tair_vertical(all_data,outnames)
        plot_sw_hrate_vertical(all_data,outnames)
        plot_lw_hrate_vertical(all_data,outnames)
        plot_tot_hrate_vertical(all_data,outnames)
        plt.close()

outpath = "/g/data3/w48/dm5220/data/figures"
input_folder = "/g/data/w48/dm5220/data"
files = [
    "ctl",
    "4co2",
    "4co2_solar50-",
    "4co2_sw_x0.9452_offset",
    "ctl_solar50+_sw-_x0.9489_offset",
    "ctl_solar50-_sw+_x1.0555_offset",
]
outnames = [
        "4co2",
        "4co2_solar-",
        "4co2_sw-",
        "sw-_solar+",
        "sw+_solar-"
]
anomalies = lambda x,y,var: my.DataArray(x[var]-y[var])

if __name__ == "__main__":
        if hasattr(sys,'ps1'): #If python is run in interactive mode
                all_data=read_data(input_folder,files)
        else: #If not
                all_data=read_data_parallel(input_folder,files)
        ctl = all_data.pop(0)
        all_plots()