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

# VERTICAL PROFILES
# Air Temperature
print(f"Plotting Air Temperature vertical profiles")
fig=plt.figure()
for data,outname in zip(all_data,all_names):
        anomalies(data,ctl,"air_temperature").annual_mean(20*12).global_mean().isel(pressure=slice(2,None)).plot(y="pressure",yincrease=False,yscale="log",label=f"{outname}")
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
for data,outname in zip(all_data,all_names):
        (anomalies(data,ctl,"tendency_of_air_temperature_due_to_shortwave_heating")*alpha).annual_mean(20*12).global_mean().isel(model_level_number=slice(None,32)).plot(y="model_level_number",label=f"{outname}")
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
for data,outname in zip(all_data,all_names):
        (anomalies(data,ctl,"tendency_of_air_temperature_due_to_longwave_heating")*alpha).annual_mean(20*12).global_mean().isel(model_level_number=slice(None,32)).plot(y="model_level_number",label=f"{outname}")
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