import multiprocessing
import concurrent.futures
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
fun = lambda x: x.surface_temperature[34,42,10].values
names = ["ctl","4co2","4co2_solar50-","4co2_sw_x0.9452_offset","ctl_solar50+_sw-_x0.95","ctl_solar50-_sw+_x1.052"]

@timer
def read_all_data():
        ctl=my.open_mfdataset(os.path.join(input_folder,"ctl/*_pa*.nc"),
                parallel=True,concat_dim="time")
        co2x4=my.open_mfdataset(os.path.join(input_folder,"4co2/*_pa*.nc"),
                parallel=True,concat_dim="time")
        solar=my.open_mfdataset(os.path.join(input_folder,"4co2_solar50-/*_pa*.nc"),
                parallel=True,concat_dim="time")
        sw=my.open_mfdataset(os.path.join(input_folder,"4co2_sw_x0.9452_offset/*_pa*.nc"),
                parallel=True,concat_dim="time")
        sw_minus=my.open_mfdataset(os.path.join(input_folder,"ctl_solar50+_sw-_x0.95/*_pa*.nc"),
                parallel=True,concat_dim="time")        
        sw_plus=my.open_mfdataset(os.path.join(input_folder,"ctl_solar50-_sw+_x1.052/*_pa*.nc"),
                parallel=True,concat_dim="time")
        return [fun(a) for a in (co2x4,solar,sw,sw_plus,sw_minus)]
                
def read_single_data(name):
        print(f"Process {os.getpid()} reading '{name}'")
        data = my.open_mfdataset(os.path.join(input_folder,f"{name}/*_pa*.nc"),
                parallel=True,concat_dim="time")
        print(f"Process {os.getpid()} done reading '{name}'")        
        return fun(data)

@timer
def main():
        return [read_single_data(name) for name in names]

@timer
def main_parallel_mt():
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                result=executor.map(read_single_data,names)
        return result

@timer
def main_parallel_mp():
        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
                result=executor.map(read_single_data,names)
        return result

if __name__ == '__main__':        
        data0 = read_all_data()
        data1 = main()
        data2 = main_parallel_mt()
        data3 = main_parallel_mp()

        for i in range(4):
                print(f"Result of data{i} is:",eval(f"data{i}"))
