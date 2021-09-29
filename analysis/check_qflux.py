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
from decorators import timer


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

def energy_balance_toa(x):
        g=lambda a: a.groupby("time.year").mean("time")
        D=lambda d: g(d.toa_outgoing_shortwave_flux) + g(d.toa_outgoing_longwave_flux) - g(d.toa_incoming_shortwave_flux)
        return D(x)

input_folder = "/g/data/w48/dm5220/data"
ctl=read_data(input_folder,["ctl"])[0]
toa_balance=energy_balance_toa(ctl)
qflux=my.open_dataarray("/g/data/w48/dm5220/ancil/qflux/qflux_slab.nc").squeeze()
qf=qflux.mean()

toa_balance.mean(["latitude","longitude"]).plot(label="Energy Balance TOA")
xlim=plt.gca().get_xlim()
plt.hlines(qf, *xlim, colors='k', ls='--',label="qflux")
plt.xlim([*xlim])
plt.ylabel("$W/m^{2}$")
plt.legend(loc=5)
yticks=plt.gca().get_yticklabels()
plt.text(1993.8,2.5,f"{qf.values:.3g}")
plt.savefig("/home/565/dm5220/qflux.png",dpi=300)

