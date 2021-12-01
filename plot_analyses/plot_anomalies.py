import myfuncs as my
import xarray as xr
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
from argparse import ArgumentParser

def read_data(file):
        data = my.open_mfdataset(
        os.path.join(
                input_folder,
                f"{file}/*_pa*.nc"),
        parallel=True,
        combine="nested",
        concat_dim="time",
        compat='override',
        coords='minimal',
        )
        return data

# SURFACE TEMP
def plot_tsurf(data,outname):        
        print(f"Plotting Surface Temperature for {outname}")
        data=anomalies(data,"surface_temperature")
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
def plot_precip(data,outname):        
        print(f"Plotting Precipitation for {outname}")
        data=anomalies(data,"precipitation_flux")
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
def plot_tair_longmean_plev(data,outname):
        var = "air_temperature_0_plev"
        if var not in data: return
        print(f"Plotting Air Temperature (longmean) for {outname} on pressure levels")
        data = anomalies(data,var)
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (longitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{outname}_tair_longmean_plev.png")
                )
        plt.clf()
        collect()

def plot_tair_longmean_mlev(data,outname):
        var = "air_temperature_0"
        if var not in data: return
        print(f"Plotting Air Temperature (longmean) for {outname} on model levels")
        data = anomalies(data,var)
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (longitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{outname}_tair_longmean_mlev.png")
                )
        plt.clf()
        collect()

def plot_tair_latmean_plev(data,outname):
        var = "air_temperature_0_plev"
        if var not in data: return
        print(f"Plotting Air Temperature (latmean) for {outname} on pressure levels")
        data = anomalies(data,var)
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (latitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{outname}_tair_latmean_plev.png")
                )
        plt.clf()
        collect()

def plot_tair_latmean_mlev(data,outname):
        var = "air_temperature_0"
        if var not in data: return
        print(f"Plotting Air Temperature (latmean) for {outname} on model levels")
        data = anomalies(data,var)
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                cmap=my.Colormaps.div_tsurf,
                levels=np.linspace(-2,2,100),
                du=0.5,
                title="Air Temperature (latitude mean)",
                units="K",
                outpath=os.path.join(outpath,f"{outname}_tair_latmean_mlev.png")
                )
        plt.clf()
        collect()

# LW HEATING RATE
def plot_lw_hrate_longmean_plev(data,outname):
        var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if var not in data: return
        print(f"Plotting LW Heating Rate (longmean) for {outname} on pressure levels")
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_longmean_plev.png")
                )
        plt.clf()
        collect()

def plot_lw_hrate_longmean_mlev(data,outname):
        var = "tendency_of_air_temperature_due_to_longwave_heating"
        if var not in data: return
        print(f"Plotting LW Heating Rate (longmean) for {outname} on model levels")
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_longmean_mlev.png")
                )
        plt.clf()
        collect()        

def plot_lw_hrate_latmean_plev(data,outname):
        var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if var not in data: return 
        print(f"Plotting LW Heating Rate (latmean) for {outname} on pressure levels")
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_latmean_plev.png")
                )
        plt.clf()
        collect()

def plot_lw_hrate_latmean_mlev(data,outname):
        var = "tendency_of_air_temperature_due_to_longwave_heating"
        if var not in data: return 
        print(f"Plotting LW Heating Rate (latmean) for {outname} on model levels")
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="LW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_LW_hrate_latmean_mlev.png")
                )
        plt.clf()
        collect()

# SW HEATING RATE
def plot_sw_hrate_longmean_plev(data,outname):
        var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (longmean) for {outname} on pressure levels")
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_longmean_plev.png")
                )
        plt.clf()
        collect()

def plot_sw_hrate_longmean_mlev(data,outname):
        var = "tendency_of_air_temperature_due_to_shortwave_heating"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (longmean) for {outname} on model levels")
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_longmean_mlev.png")
                )
        plt.clf()
        collect()

def plot_sw_hrate_latmean_plev(data,outname):
        var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (latmean) for {outname} on pressure levels") 
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_latmean_plev.png")
                )
        plt.clf()
        collect()

def plot_sw_hrate_latmean_mlev(data,outname):
        var = "tendency_of_air_temperature_due_to_shortwave_heating"
        if var not in data: return 
        print(f"Plotting SW Heating Rate (latmean) for {outname} on model levels") 
        data = anomalies(data,var)
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_SW_hrate_latmean_mlev.png")
                )
        plt.clf()
        collect()

# TOT HEATING RATE
def plot_tot_hrate_longmean_plev(data,outname):
        var1 = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        var2 = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if (var1 not in data) or (var2 not in data): return
        print(f"Plotting TOT Heating Rate (longmean) for {outname} on pressure levels")
        data1 = anomalies(data,var1)
        data2 = anomalies(data,var2)
        data = data1+data2
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_longmean_plev.png")
                )
        plt.clf()
        collect()

def plot_tot_hrate_longmean_mlev(data,outname):
        var1 = "tendency_of_air_temperature_due_to_shortwave_heating"
        var2 = "tendency_of_air_temperature_due_to_longwave_heating"
        if (var1 not in data) or (var2 not in data): return
        print(f"Plotting TOT Heating Rate (longmean) for {outname} on model levels")
        data1 = anomalies(data,var1)
        data2 = anomalies(data,var2)
        data = data1+data2
        data = data*60*60*24
        data = data.longitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (longitude mean)",
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_longmean_mlev.png")
                )
        plt.clf()
        collect()

def plot_tot_hrate_latmean_plev(data,outname):
        var1 = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        var2 = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        if (var1 not in data) or (var2 not in data): return
        print(f"Plotting TOT Heating Rate (latmean) for {outname} on pressure levels")
        data1 = anomalies(data,var1)
        data2 = anomalies(data,var2)
        data = data1+data2
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_latmean_plev.png")
                )
        plt.clf()
        collect()

def plot_tot_hrate_latmean_mlev(data,outname):
        var1 = "tendency_of_air_temperature_due_to_shortwave_heating"
        var2 = "tendency_of_air_temperature_due_to_longwave_heating"
        if (var1 not in data) or (var2 not in data): return
        print(f"Plotting TOT Heating Rate (latmean) for {outname} on model levels")
        data1 = anomalies(data,var1)
        data2 = anomalies(data,var2)
        data = data1+data2
        data = data*60*60*24
        data = data.latitude_mean()
        data = data.annual_mean(20*12)
        data.plotlev(
                levels=np.linspace(-0.1,0.1,100),
                cmap=my.Colormaps.div_tsurf,
                du=0.02,
                units="K/day",
                title="SW Heating Rate (latitude mean)",
                outpath=os.path.join(outpath,f"{outname}_TOT_hrate_latmean_mlev.png")
                )
        plt.clf()
        collect()

# SW Radiation (TOA out) 
def plot_sw_out(data,outname):
        print(f"Plotting SW Radiation out (TOA) for {outname}")
        data = anomalies(data,"toa_outgoing_shortwave_flux")
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
def plot_lw_out(data,outname):
        print(f"Plotting LW Radiation out (TOA) for {outname}")
        data = anomalies(data,"toa_outgoing_longwave_flux")
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


def all_plots(data,outname):
        plot_tsurf(data,outname)
        plot_precip(data,outname)
        plot_tair_longmean_plev(data,outname)
        plot_tair_longmean_mlev(data,outname)
        plot_tair_latmean_plev(data,outname)
        plot_tair_latmean_mlev(data,outname)
        plot_lw_hrate_longmean_plev(data,outname)
        plot_lw_hrate_longmean_mlev(data,outname)
        plot_lw_hrate_latmean_plev(data,outname)
        plot_lw_hrate_latmean_mlev(data,outname)
        plot_sw_hrate_longmean_plev(data,outname)
        plot_sw_hrate_longmean_mlev(data,outname)
        plot_sw_hrate_latmean_plev(data,outname)
        plot_sw_hrate_latmean_mlev(data,outname)
        plot_tot_hrate_longmean_plev(data,outname)
        plot_tot_hrate_longmean_mlev(data,outname)
        plot_tot_hrate_latmean_plev(data,outname)
        plot_tot_hrate_latmean_mlev(data,outname)
        plot_lw_out(data,outname)
        plot_sw_out(data,outname)

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,nargs='*')
parser.add_argument('-o','--outnames',type=str,nargs='*')
parser.add_argument('-C','--control',type=str,default="ctl")
args=parser.parse_args()

files=args.input
outnames=args.outnames
control_file=args.control
if outnames is None:
        outnames = files
if len(files) != len(outnames):
        raise Exception(f"Number of input files and output names mismatch. \
Number of input files is {len(files)}. \
Number of output names is {len(outnames)}")
input_folder = "/g/data/w48/dm5220/data"        
outpath = "/g/data3/w48/dm5220/data/figures"
data_ctl = my.open_mfdataset(
                os.path.join(
                        input_folder,
                        f"{control_file}/*_pa*.nc"),
                parallel=True,
                combine="nested",
                concat_dim="time",
                compat='override',
                coords='minimal',
                )
anomalies = lambda x,var: my.DataArray(x[var]-data_ctl[var])

for file,outname in zip(files,outnames):
        print(f"Reading {file}...")
        data = read_data(file)
        all_plots(data,outname)
plt.close()
