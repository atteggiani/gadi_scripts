import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os
import sys
import dask
import cartopy.crs as ccrs
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

ctl=my.UM.read_data("ctl").precipitation_flux
gm=[]
rms=[]
for i in range(1,10):
    d=(my.UM.read_data(f"4co2_fix_tsurf_best{i}").precipitation_flux - ctl).annual_mean(20*12,normalize=True).to_mm_per_day()
    gm.append(d.global_mean().values)
    rms.append(d.rms().values)
    del d

plt.plot(gm,marker='o')
plt.title('Global Mean')
plt.xticks(np.arange(9),labels=[f'Best{i}' for i in np.arange(1,10)])
plt.grid()
plt.savefig("")
