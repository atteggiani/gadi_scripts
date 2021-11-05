import myfuncs as my
import xarray as xr
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
import concurrent.futures
import dask
from dask.diagnostics import ProgressBar
from decorators import timed
from metpy.interpolate import log_interpolate_1d
from metpy.units import units
from scipy.interpolate import interp1d
import matplotlib.colors as colors
from importlib import reload

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

def plot_vertical_profiles(all_data,labels=None,colors=None,**kwargs):
    if isinstance(all_data,xr.DataArray):
        all_data=[all_data]
    dims=[a.dims for a in all_data]
    cond=[d==dims[0] for d in dims]
    if not all(cond):
        raise Exception("Dimensions of different data mismatch.")
    if "pressure" in dims[0]:
        selection =lambda x: x.sel(pressure=slice(49,1001))
        y="pressure"
        vline=lambda x: x.vlines(0, 50, 1000, colors='k', ls='--',lw=0.8)
        ylim=[1000,50]
        yticks=np.array([1000,800,600,400,200,50])
        ylabel="pressure [hPa]"
        yscale="log"
        yincrease=False
    elif "model_level_number" in dims[0]:
        selection =lambda x: x.sel(model_level_number=slice(-0.5,32.5))
        y="model_level_number"
        vline=lambda x: x.vlines(0, 1, 32, colors='k', ls='--',lw=0.8)
        ylim=[1,32]
        yticks=np.arange(1,32,5)
        ylabel="Model Level Number"
        yscale="linear"
        yincrease=True
    else:
        raise Exception("No vertical levels found in data.")

    if labels is None:
        labels = [f"data{i+1}" for i in range(len(all_data))]
    if colors is None:
        colors = [None for _ in range(len(all_data))]
    for d,label,color in zip(all_data,labels,colors):
            data = selection(d)
            data.plot(
                    y=y,
                    yincrease=yincrease,
                    yscale=yscale,
                    label=label,
                    color=color,
                    **kwargs,
                    )

    vline(plt)
    plt.ylim(ylim)
    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels(yticks.tolist())
    plt.grid(ls="--",which='both')
    plt.ylabel(ylabel)

input_folder = "/g/data/w48/dm5220/data"
outpath = "/g/data3/w48/dm5220/data/figures/seasonal_hrates"
input_folder = "/g/data/w48/dm5220/data"
files = [
    "ctl",
    # "4co2",
    "4co2_solar50-",
    "4co2_sw_x0.9452_offset",
    # "ctl_solar50+_sw-_x0.9489_offset",
    # "ctl_solar50-_sw+_x1.0555_offset",
]

data=read_data(input_folder,files)
ctl=data.pop(0)
anomalies = lambda x,var: my.DataArray(x[var]-ctl[var])

lwh="tendency_of_air_temperature_due_to_longwave_heating_plev"
swh="tendency_of_air_temperature_due_to_shortwave_heating_plev"
solar=data[0]
sw=data[1]
alpha=60*60*24

solar_LWhrate=anomalies(solar,lwh)*alpha
solar_SWhrate=anomalies(solar,swh)*alpha
solar_TOThrate=solar_SWhrate+solar_LWhrate

sw_LWhrate=anomalies(sw,lwh)*alpha
sw_SWhrate=anomalies(sw,swh)*alpha
sw_TOThrate=sw_SWhrate+sw_LWhrate

all_data=[solar_LWhrate,solar_SWhrate,solar_TOThrate,
          sw_LWhrate,sw_SWhrate,sw_TOThrate]
all_labels=['4co2_solar-_LW','4co2_solar-_SW','4co2_solar-_TOT',
            '4co2_sw-_LW','4co2_sw-_SW','4co2_sw-_TOT',]
all_titles=['4co2 & Solar-']*3 + ['4co2 & SW-']*3
all_vars=['LW','SW','TOT']*2
colourlist=['magenta', 'pink', 'mediumorchid', 'mediumslateblue', 'b',
       'deepskyblue', 'turquoise', 'green', 'limegreen', 'greenyellow',
       'y', 'khaki', 'darkorange', 'tomato', 'red', 'black']

# ANNUAL CYCLE
def annual_cyc():
    for data,label,tit,var in zip(all_data,all_labels,all_titles,all_vars):
        plt.figure()
        for i,p in enumerate(data.pressure):
            data.global_mean().groupby('time.month').mean('time').sel(pressure=p).plot(
                label=f"{p.values:g} hPa",
                color=colourlist[i],
                )
        plt.legend(loc='lower left',bbox_to_anchor=(1.05,-0.1))
        plt.xlim(1,12)
        plt.xticks(range(1,13),labels=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'],fontsize=8)
        plt.ylabel('K/day')
        plt.grid(ls="--")
        plt.title(f'{var} Heating Rate | {tit}',fontsize=12)
        plt.savefig(os.path.join(outpath,f'{label}_annual_cycle_all-levs'),bbox_inches='tight',dpi=300)
        #plt.show()
        plt.clf()

# SEASONAL PROFILES
def seas_prof():
    for d in ['LW', 'SW', 'TOT']:
        if d == 'LW':
            seas_data = [f for f in solar_LWhrate.groupby('time.season').mean('time').global_mean()] + \
                        [f for f in sw_LWhrate.groupby('time.season').mean('time').global_mean()]
        elif d == 'SW':
            seas_data = [f for f in solar_SWhrate.groupby('time.season').mean('time').global_mean()] + \
                        [f for f in sw_SWhrate.groupby('time.season').mean('time').global_mean()]
        else:
            seas_data = [f for f in solar_TOThrate.groupby('time.season').mean('time').global_mean()] + \
                        [f for f in sw_TOThrate.groupby('time.season').mean('time').global_mean()]
        
        labels=["4co2 & Solar-","4co2 & SW-"]
        seasons=['DJF', 'JJA', 'MAM', 'SON']
        all_labels=[f'{l} {s}' for l in labels for s in seasons]
        all_colors=['darkorange','orange','gold','moccasin',
                'darkgreen','forestgreen','limegreen','lightgreen']

        plt.figure()
        plot_vertical_profiles(seas_data,
                        labels=all_labels,
                        colors=all_colors)
        plt.xlabel('K/day')
        plt.xlim([-0.1,0.2])
        plt.xticks(np.arange(-0.1,0.2+0.025,0.025),fontsize=8)
        plt.title(f'{d} Heating Rates | Vertical profiles')
        plt.legend(loc='upper left',bbox_to_anchor=(1.05,1))
        plt.savefig(os.path.join(outpath,f'{d}_vertical_profiles_seasons'),bbox_inches='tight',dpi=300)
        # plt.show()
        plt.clf()

# VERTICAL PROFILES FILLED
def vert_prof():
    for d in ['LW', 'SW', 'TOT']:
        data2 = [eval(f'solar_{d}hrate').groupby('time.season').mean('time').global_mean(),
                eval(f'sw_{d}hrate').groupby('time.season').mean('time').global_mean()]
        dmin=[da.min('season') for da in data2]
        dmax=[da.max('season') for da in data2]
        dmean=[da.mean('season') for da in data2]

        labels=["4co2 & Solar-","4co2 & SW-"]
        colors=['darkorange','darkgreen']
        seas_var_colors=['darkorange','darkgreen']
        seas_var_alpha=0.3

        plt.figure()
        plot_vertical_profiles(dmean,
                        labels=labels,
                        colors=colors,
                        lw=0.6)
        for da,dm,dM,c in zip(dmean,dmin,dmax,colors):
            plt.fill_betweenx(y=da.pressure, x1=dm, x2=dM, color=c, alpha=seas_var_alpha)
        plt.xlabel('K/day')
        plt.xlim([-0.1,0.2])
        plt.xticks(np.arange(-0.1,0.2+0.025,0.025),fontsize=8)
        plt.title(f'{d} Heating Rates | Vertical profiles')
        plt.legend(loc='upper left',bbox_to_anchor=(1.05,1))
        plt.savefig(os.path.join(outpath,f'{d}_vertical_profiles_filled'),bbox_inches='tight',dpi=300)
        # plt.show()
        plt.clf()

seas_prof()
vert_prof()