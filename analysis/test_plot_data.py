import multiprocessing
import concurrent.futures

from pandas.core.indexes.api import all_indexes_same
from decorators import timer
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect
import time

outpath = "/g/data3/w48/dm5220/data/figures"
input_folder = "/g/data/w48/dm5220/data"
names = ["ctl","4co2","4co2_solar50-","4co2_sw_x0.9452_offset","ctl_solar50+_sw-_x0.95","ctl_solar50-_sw+_x1.052"]

def read_single_data(input_folder,name):
    print(f"Process {os.getpid()} reading '{name}'")
    data = my.open_mfdataset(os.path.join(input_folder,f"{name}/*_pa*.nc"),
            parallel=True,concat_dim="time")
    print(f"Process {os.getpid()} done reading '{name}'")        
    return data

# def read_all_data():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
#             result=executor.map(read_single_data,names)
#     return result

all_data = {name:read_single_data(input_folder,name) for name in names}

def plot_annual_mean(name,data_variable):
    print(f"Process {os.getpid()} plotting '{data_variable}' of '{name}'")
    data = my.DataArray(all_data[name][data_variable])
    im=data.annual_mean(-20*12).plotvar()
    print(f"Process {os.getpid()} done plotting '{data_variable}' of '{name}'")
    return im

@timer
def main():
    [plot_annual_mean(name,"surface_temperature") for name in names]

@timer
def main_parallel_mt():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(lambda x: plot_annual_mean(x,"surface_temperature"),names)

@timer
def main_parallel_mp():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(lambda x: plot_annual_mean(x,"surface_temperature"),names)

if __name__ == "__main__":
    main()
    main_parallel_mt()
    main_parallel_mp()
