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

best="best29"
outfile_suffix="35-38"

ind=[int(a) for a in outfile_suffix.split('-')]
indeces=range(ind[0],ind[1]+1)
outdir="/g/data3/w40/dm5220/data/figures/anomalies"
ctl=my.UM.read_data("ctl").precipitation_flux.to_mm_per_day()
data=[]
gm=[]
gm_tr=[]
gm_nh=[]
gm_sh=[]
rms=[]
rms_tr=[]
rms_nh=[]
rms_sh=[]

data.append(my.UM.read_data(f"4co2_fix_tsurf").precipitation_flux.to_mm_per_day())
d=(data[-1] - ctl).annual_mean(20*12,normalize=True)
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
label=best[0].upper()+best[1:]

d=(my.UM.read_data(f"4co2_fix_tsurf_{best}").precipitation_flux.to_mm_per_day() - ctl).annual_mean(20*12,normalize=True)
data.append(d)
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

for i in indeces:
    try:
        d=(my.UM.read_data(f"4co2_fix_tsurf_best{i}").precipitation_flux.to_mm_per_day() - ctl).annual_mean(20*12,normalize=True)
    except OSError:
        gm.append(np.nan)
        rms.append(np.nan)
        gm_tr.append(np.nan)
        rms_tr.append(np.nan)
        gm_nh.append(np.nan)
        rms_nh.append(np.nan)
        gm_sh.append(np.nan)
        rms_sh.append(np.nan)
        continue

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
ax1.set_xticklabels(['NO_FLUX',label]+[f'Best{i}' for i in indeces], fontsize=8, rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,f"custom_exp_gm_rms_global_{outfile_suffix}"),dpi=300,bbox_inches='tight')

# PLOT TROPICS
fig, ax1 = plt.subplots()
plt.title('Tropics (30°S÷30°N)')
color='blue'
ax1.plot(gm_tr,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm_tr)))
ax1.set_xticklabels(['NO_FLUX',label]+[f'Best{i}' for i in indeces],fontsize=8,rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms_tr,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,f"custom_exp_gm_rms_tropics_{outfile_suffix}"),dpi=300,bbox_inches='tight')

# PLOT NORTHERN HEMISPHERE
fig, ax1 = plt.subplots()
plt.title('Northern Hemisphere (30°N÷90°N)')
color='blue'
ax1.plot(gm_nh,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm_nh)))
ax1.set_xticklabels(['NO_FLUX',label]+[f'Best{i}' for i in indeces],fontsize=8,rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms_nh,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,f"custom_exp_gm_rms_NHem_{outfile_suffix}"),dpi=300,bbox_inches='tight')

# PLOT SOUTHERN HEMISPHERE
fig, ax1 = plt.subplots()
plt.title('Southern Hemisphere (90°S÷30°S)')
color='blue'
ax1.plot(gm_sh,marker='o',color=color)
ax1.set_xticks(np.arange(len(gm_sh)))
ax1.set_xticklabels(['NO_FLUX',label]+[f'Best{i}' for i in indeces],fontsize=8,rotation=90)
ax1.set_ylabel('Global Mean $[mm \cdot d^{-1}]$',color=color)
ax1.grid()

ax2 = ax1.twinx()
color='green'
ax2.plot(rms_sh,marker='o',color=color)
ax2.set_ylabel('RMS',color=color)

fig.tight_layout()
plt.savefig(os.path.join(outdir,f"custom_exp_gm_rms_SHem_{outfile_suffix}"),dpi=300,bbox_inches='tight')

