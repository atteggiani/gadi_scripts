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

outpath = "/g/data3/w48/dm5220/data/figures"
input_folder = "/g/data/w48/dm5220/data"
files = [
    "ctl",
    "4co2",
    "4co2_solar50-",
    "4co2_sw_x0.9452_offset",
    "ctl_solar50+_sw-_x0.95",
    "ctl_solar50-_sw+_x1.0555_offset",
]
outnames = [
        "4co2",
        "solar",
        "sw",
        "sw-_solar+",
        "sw+_solar-"
]

if hasattr(sys,'ps1'): #If python is run in interactive mode
        all_data=read_data(input_folder,files)
else: #If not
        all_data=read_data_parallel(input_folder,files)
ctl = all_data.pop(0)
anomalies = lambda x,var: my.DataArray(x[var]-ctl[var])

D=lambda d: g(d.toa_incoming_shortwave_flux) - (g(d.toa_outgoing_shortwave_flux) + g(d.toa_outgoing_longwave_flux))
g=lambda a: a.groupby("time.year").mean("time")

D(all_data[0]).mean(["latitude","longitude"]).plot()