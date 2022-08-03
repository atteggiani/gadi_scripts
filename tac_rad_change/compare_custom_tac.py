import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os
import glob
import sys
import dask
import cartopy.crs as ccrs
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import concurrent.futures
import time

t1=time.perf_counter()
files=glob.glob("/g/data3/w40/dm5220/data/4co2_fix_tsurf_best*")
indeces=[int(f.split('/g/data3/w40/dm5220/data/4co2_fix_tsurf_best')[1]) for f in files]
indeces,files=[a[0] for a in sorted(zip(indeces,files))],[a[1] for a in sorted(zip(indeces,files))]
outdir="/g/data3/w40/dm5220/data/figures/anomalies"
ctl=my.UM.read_data("ctl").precipitation_flux.to_mm_per_day()
gm=[]
gm_tr=[]
gm_nh=[]
gm_sh=[]
rms=[]
rms_tr=[]
rms_nh=[]
rms_sh=[]

d=(my.UM.read_data(f"4co2_fix_tsurf").precipitation_flux.to_mm_per_day() - ctl).annual_mean(20*12,normalize=True)
tr=d.sel(latitude=slice(-30,30))
nh=d.sel(latitude=slice(30,90))
sh=d.sel(latitude=slice(-90,-30))
gm.append(d.global_mean().values)
rms.append(d.rms().values)
gm_tr.append(tr.global_mean().values)
rms_tr.append(tr.rms().values)
gm_nh.append(nh.global_mean().values)
rms_nh.append(nh.rms().values)
gm_sh.append(sh.global_mean().values)
rms_sh.append(sh.rms().values)

for f in files:
    d=(my.UM.read_data(f).precipitation_flux.to_mm_per_day() - ctl).annual_mean(20*12,normalize=True)
    gm.append(d.global_mean().values)
    rms.append(d.rms().values)
    tr=d.sel(latitude=slice(-30,30))
    nh=d.sel(latitude=slice(30,90))
    sh=d.sel(latitude=slice(-90,-30))
    gm_tr.append(tr.global_mean().values)
    rms_tr.append(tr.rms().values)
    gm_nh.append(nh.global_mean().values)
    rms_nh.append(nh.rms().values)
    gm_sh.append(sh.global_mean().values)
    rms_sh.append(sh.rms().values)

# PLOT GLOBAL
fig, ax1 = plt.subplots()
plt.title('Global')
color='blue'
ax1.plot(gm,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm)))
ax1.set_xticklabels(['NO_FLUX']+[f'Best{i}' for i in indeces], fontsize=8, rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,"custom_exp_gm_rms_global"),dpi=300,bbox_inches='tight')

# PLOT TROPICS
fig, ax1 = plt.subplots()
plt.title('Tropics (30°S÷30°N)')
color='blue'
ax1.plot(gm_tr,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm_tr)))
ax1.set_xticklabels(['NO_FLUX']+[f'Best{i}' for i in indeces],fontsize=8,rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms_tr,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,"custom_exp_gm_rms_tropics"),dpi=300,bbox_inches='tight')

# PLOT NORTHERN HEMISPHERE
fig, ax1 = plt.subplots()
plt.title('Northern Hemisphere (30°N÷90°N)')
color='blue'
ax1.plot(gm_nh,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm_nh)))
ax1.set_xticklabels(['NO_FLUX']+[f'Best{i}' for i in indeces],fontsize=8,rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms_nh,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,"custom_exp_gm_rms_NHem"),dpi=300,bbox_inches='tight')

# PLOT SOUTHERN HEMISPHERE
fig, ax1 = plt.subplots()
plt.title('Southern Hemisphere (90°S÷30°S)')
color='blue'
ax1.plot(gm_sh,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm_sh)))
ax1.set_xticklabels(['NO_FLUX']+[f'Best{i}' for i in indeces],fontsize=8,rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms_sh,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,"custom_exp_gm_rms_SHem"),dpi=300,bbox_inches='tight')

t2=time.perf_counter()
print(f"Finished in {t2-t1} seconds")