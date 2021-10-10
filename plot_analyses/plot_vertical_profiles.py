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
from argparse import ArgumentParser

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

# VERTICAL PROFILES
# Air Temperature
def tair(all_data,all_labels,outname):
        print(f"Plotting Air Temperature vertical profiles")
        cond=["air_temperature_0_plev" in data for data in all_data] 
        if np.all(cond):
                var = "air_temperature_0_plev"
        else:
                var = "air_temperature"
        for data,label in zip(all_data,all_labels):
                data = anomalies(data,var)
                data = data.sel(pressure=slice(49,1001))
                data = data.annual_mean(20*12)
                data = data.global_mean()
                data.plot(
                        y="pressure",
                        yincrease=False,
                        yscale="log",
                        label=f"{label}")                        
        plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        plt.ylim([1000,50])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(
                ["{}".format(i) for i in [1000,800,600,400,200,50]])
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K")
        plt.title("Air Temperature Vertical Profiles")
        plt.savefig(os.path.join(outpath,f"{outname}_vertical_profiles.png"),
                    dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting Air Temperature vertical profiles")

# SW Heating Rates
def sw_hrate(all_data,all_labels,outname):
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
                yscale="linar"
                yincrease=True

        for data,label in zip(all_data,all_labels):
                data = anomalies(data,var)
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
        plt.gca().set_yticks(yticks)
        plt.gca().set_yticklabels(yticks.tolist())
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Model Level Number")
        plt.title("SW Heating Rate Vertical Profiles")
        plt.savefig(os.path.join(outpath,f"{outname}_vertical_profiles.png"),
                    dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting SW Heating Rate vertical profiles")

# LW Heating Rates
def lw_hrate(all_data,all_labels,outname):
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
                yscale="linar"
                yincrease=True
        for data,label in zip(all_data,all_labels):
                data = anomalies(data,var)
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
        plt.gca().set_yticks(yticks)
        plt.gca().set_yticklabels(yticks.tolist())
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Model Level Number")
        plt.title("LW Heating Rate Vertical Profiles")
        plt.savefig(os.path.join(outpath,f"{outname}_vertical_profiles.png"),
                    dpi=300)
        plt.clf()
        collect()
        print(f"Done plotting LW Heating Rate vertical profiles")

def all_plots(outnames):
        tair(all_data,all_labels,outnames[0])
        sw_hrate(all_data,all_labels,outnames[1])
        lw_hrate(all_data,all_labels,outnames[2])
        plt.close()

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,nargs='*')
parser.add_argument('-l','--labels',type=str,nargs='*')
parser.add_argument('-o','--output',type=str,nargs='*')
parser.add_argument('-c','--control',type=str,default="ctl")
args=parser.parse_args()

files=args.input
all_labels=args.labels
outnames=args.output
if outnames is None: outnames = ["tair","sw_hrate","lw_hrate"]
control_file=args.control
if all_labels is None:
        all_labels = files

if len(files) != len(all_labels):
        raise Exception(f"Number of input files and output labels mismatch. \
Number of input files is {len(files)}. \
Number of output labels is {len(all_labels)}")

outpath = "/g/data3/w48/dm5220/data/figures"
input_folder = "/g/data/w48/dm5220/data"
files = [control_file]+files
# files=[
#         "ctl",
#         "4co2",
#         "4co2_solar50-",
#         "4co2_sw_x0.9452_offset",
#         "ctl_solar50+_sw-_x0.95",
#         "ctl_solar50-_sw+_x1.0555_offset"]

if hasattr(sys,'ps1'): #If python is run in interactive mode
        all_data=read_data(input_folder,files)
else: #If not
        all_data=read_data_parallel(input_folder,files)
ctl = all_data.pop(0)
anomalies = lambda x,var: my.DataArray(x[var]-ctl[var])

if __name__ == "__main__":
        all_plots(outnames)