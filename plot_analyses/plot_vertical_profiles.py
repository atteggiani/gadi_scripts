import myfuncs as my
import xarray as xr
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from gc import collect
import concurrent.futures
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
def tair_plev(all_data,all_labels,outname):
        var = "air_temperature_0_plev"
        cond=[var in data for data in all_data] 
        if not np.all(cond): return
        print(f"Plotting Air Temperature vertical profiles on pressure levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data = anomalies(data,var)
                data = data.sel(pressure=slice(49,1001))
                data = data.global_mean()
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am.plot(
                        y="pressure",
                        yincrease=False,
                        yscale="log",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.pressure, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        plt.ylim([1000,50])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(
                ["{}".format(i) for i in [1000,800,600,400,200,50]])
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K")
        plt.ylabel("Pressure [hPa]")
        plt.title("Air Temperature Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"tair_vertprof_plev.png"])
        else:
                outname="tair_vertprof_plev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

def tair_mlev(all_data,all_labels,outname):
        var = "air_temperature_0"
        cond=[var in data for data in all_data] 
        if not np.all(cond): return
        print(f"Plotting Air Temperature vertical profiles on model levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data = anomalies(data,var)
                data = data.sel(model_level_number=slice(None,32))
                data = data.global_mean()
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am = am.assign_coords(model_level_number=np.arange(32))
                am.plot(
                        y="model_level_number",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.model_level_number, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 0, 31, colors='k', ls='--',lw=0.8)
        plt.ylim([0,31])
        plt.gca().set_yticks(np.arange(0,32))
        ticklabels=[str(i) for i in np.arange(1,33)];ticklabels[1::2]=["" for _ in ticklabels[1::2]]
        plt.gca().set_yticklabels(ticklabels,fontsize=8)
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K")
        plt.ylabel("Model Level Number")
        plt.title("Air Temperature Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"tair_vertprof_mlev.png"])
        else:
                outname="tair_vertprof_mlev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

# SW Heating Rates
def sw_hrate_plev(all_data,all_labels,outname):
        var = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        cond=[var in data for data in all_data] 
        if not np.all(cond): return
        print(f"Plotting SW Heating Rate vertical profiles on pressure levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data = anomalies(data,var)
                data = data.sel(pressure=slice(49,1001))
                data = data.global_mean()
                data = data*60*60*24
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am.plot(
                        y="pressure",
                        yincrease=False,
                        yscale="log",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.pressure, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        plt.ylim([1000,50])
        plt.xlim([-0.4,0.3])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(
                ["{}".format(i) for i in [1000,800,600,400,200,50]])
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Pressure [hPa]")
        plt.title("SW Heating Rate Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"swhrate_vertprof_plev.png"])
        else:
                outname="swhrate_vertprof_plev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

def sw_hrate_mlev(all_data,all_labels,outname):
        var = "tendency_of_air_temperature_due_to_shortwave_heating"
        cond=[var in data for data in all_data] 
        if not np.all(cond): return
        print(f"Plotting SW Heating Rate vertical profiles on model levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data = anomalies(data,var)
                data = data.sel(model_level_number=slice(None,32))
                data = data.global_mean()
                data = data*60*60*24
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am = am.assign_coords(model_level_number=np.arange(32))
                am.plot(
                        y="model_level_number",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.model_level_number, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 0, 31, colors='k', ls='--',lw=0.8)
        plt.ylim([0,31])
        plt.xlim([-0.4,0.3])
        plt.gca().set_yticks(np.arange(0,32))
        ticklabels=[str(i) for i in np.arange(1,33)];ticklabels[1::2]=["" for _ in ticklabels[1::2]]
        plt.gca().set_yticklabels(ticklabels,fontsize=8)
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Model Level Number")
        plt.title("SW Heating Rate Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"swhrate_vertprof_mlev.png"])
        else:
                outname="swhrate_vertprof_mlev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

# LW Heating Rates
def lw_hrate_plev(all_data,all_labels,outname):
        var = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        cond=[var in data for data in all_data] 
        if not np.all(cond): return
        print(f"Plotting LW Heating Rate vertical profiles on pressure levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data = anomalies(data,var)
                data = data.sel(pressure=slice(49,1001))
                data = data.global_mean()
                data = data*60*60*24
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am.plot(
                        y="pressure",
                        yincrease=False,
                        yscale="log",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.pressure, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        plt.ylim([1000,50])
        plt.xlim([-0.4,0.3])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(
                ["{}".format(i) for i in [1000,800,600,400,200,50]])
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Pressure [hPa]")
        plt.title("LW Heating Rate Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"lwhrate_vertprof_plev.png"])
        else:
                outname="lwhrate_vertprof_plev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

def lw_hrate_mlev(all_data,all_labels,outname):
        var = "tendency_of_air_temperature_due_to_longwave_heating"
        cond=[var in data for data in all_data] 
        if not np.all(cond): return
        print(f"Plotting LW Heating Rate vertical profiles on model levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data = anomalies(data,var)
                data = data.sel(model_level_number=slice(None,32))
                data = data.global_mean()
                data = data*60*60*24
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am = am.assign_coords(model_level_number=np.arange(32))
                am.plot(
                        y="model_level_number",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.model_level_number, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 0, 31, colors='k', ls='--',lw=0.8)
        plt.ylim([0,31])
        plt.xlim([-0.4,0.3])
        plt.gca().set_yticks(np.arange(0,32))
        ticklabels=[str(i) for i in np.arange(1,33)];ticklabels[1::2]=["" for _ in ticklabels[1::2]]
        plt.gca().set_yticklabels(ticklabels,fontsize=8)
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Model Level Number")
        plt.title("LW Heating Rate Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"lwhrate_vertprof_mlev.png"])
        else:
                outname="lwhrate_vertprof_mlev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

# TOT Heating Rates
def tot_hrate_plev(all_data,all_labels,outname):
        var1 = "tendency_of_air_temperature_due_to_shortwave_heating_plev"
        var2 = "tendency_of_air_temperature_due_to_longwave_heating_plev"
        cond1=[var1 in data for data in all_data]
        cond2=[var2 in data for data in all_data]
        if not np.all(cond1) or not np.all(cond2): return
        print(f"Plotting TOT Heating Rate vertical profiles on pressure levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data1 = anomalies(data,var1)
                data2 = anomalies(data,var2)
                data = data1+data2
                data = data.sel(pressure=slice(49,1001))
                data = data.global_mean()
                data = data*60*60*24
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am.plot(
                        y="pressure",
                        yincrease=False,
                        yscale="log",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.pressure, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        plt.ylim([1000,50])
        plt.xlim([-0.4,0.3])
        plt.gca().set_yticks([1000,800,600,400,200,50])
        plt.gca().set_yticklabels(
                ["{}".format(i) for i in [1000,800,600,400,200,50]])
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Pressure [hPa]")
        plt.title("Total (SW + LW) Heating Rate Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"tothrate_vertprof_plev.png"])
        else:
                outname="tothrate_vertprof_plev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()

def tot_hrate_mlev(all_data,all_labels,outname):
        var1 = "tendency_of_air_temperature_due_to_shortwave_heating"
        var2 = "tendency_of_air_temperature_due_to_longwave_heating"
        cond1=[var1 in data for data in all_data]
        cond2=[var2 in data for data in all_data]
        if not np.all(cond1) or not np.all(cond2): return
        print(f"Plotting TOT Heating Rate vertical profiles on model levels")
        for data,label,color in zip(all_data,all_labels,colors[:len(all_data)]):
                data1 = anomalies(data,var1)
                data2 = anomalies(data,var2)
                data = data1+data2
                data = data.sel(model_level_number=slice(None,32))
                data = data.global_mean()
                data = data*60*60*24
                am = data.annual_mean(20*12)
                min=data.isel(time=slice(-20*12,None)).min('time')
                max=data.isel(time=slice(-20*12,None)).max('time')
                am = am.assign_coords(model_level_number=np.arange(32))
                am.plot(
                        y="model_level_number",
                        label=label,
                        color=color)
                plt.fill_betweenx(y=am.model_level_number, x1=min, x2=max,
                                        color=color, alpha=0.2)

        plt.vlines(0, 0, 31, colors='k', ls='--',lw=0.8)
        plt.ylim([0,31])
        plt.gca().set_yticks(np.arange(0,32))
        ticklabels=[str(i) for i in np.arange(1,33)];ticklabels[1::2]=["" for _ in ticklabels[1::2]]
        plt.gca().set_yticklabels(ticklabels,fontsize=8)
        plt.grid(ls="--",which='both')
        plt.legend()
        plt.xlabel("K/day")
        plt.ylabel("Model Level Number")
        plt.title("Total (SW + LW) Heating Rate Vertical Profiles")
        if outname is not None: 
                outname="_".join([outname,"tothrate_vertprof_mlev.png"])
        else:
                outname="tothrate_vertprof_mlev.png"
        plt.savefig(os.path.join(outpath,outname),dpi=300)
        plt.clf()
        collect()


def all_plots(all_data,all_labels,outname):
        tair_plev(all_data,all_labels,outname)
        tair_mlev(all_data,all_labels,outname)
        sw_hrate_plev(all_data,all_labels,outname)
        sw_hrate_mlev(all_data,all_labels,outname)
        lw_hrate_plev(all_data,all_labels,outname)
        lw_hrate_mlev(all_data,all_labels,outname)
        tot_hrate_plev(all_data,all_labels,outname)
        tot_hrate_mlev(all_data,all_labels,outname)
        plt.close()

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,nargs='*')
parser.add_argument('-l','--labels',type=str,nargs='*')
parser.add_argument('-o','--outname',type=str)
parser.add_argument('-C','--control',type=str,default="ctl")
parser.add_argument('-c','--colors',type=str,nargs='*')
args=parser.parse_args()

files=args.input
all_labels=args.labels
outname=args.outname
colors=args.colors
if colors is None: colors=['blue','darkorange','firebrick','darkgreen','m','turquoise',
       'rebeccapurple', 'grey']
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
        all_plots(all_data,all_labels,outname)

        