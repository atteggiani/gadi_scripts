import multiprocessing
import concurrent.futures
import xarray as xr
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from gc import collect

def timer(func):
    """Print the runtime of the decorated function"""
    from functools import wraps
    import time
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

outpath = "/g/data3/w48/dm5220/data/figures"
input_folder = "/g/data/w48/dm5220/data"
fun = lambda x: x.surface_temperature[34,42,10].values
files = ["ctl","4co2","4co2_solar50-","4co2_sw_x0.9452_offset","ctl_solar50+_sw-_x0.95","ctl_solar50-_sw+_x1.052"]

@timer
def read_all_data():
        ctl=xr.open_mfdataset(os.path.join(input_folder,"ctl/*_pa*.nc"),
                parallel=True,concat_dim="time")
        co2x4=xr.open_mfdataset(os.path.join(input_folder,"4co2/*_pa*.nc"),
                parallel=True,concat_dim="time")
        solar=xr.open_mfdataset(os.path.join(input_folder,"4co2_solar50-/*_pa*.nc"),
                parallel=True,concat_dim="time")
        sw=xr.open_mfdataset(os.path.join(input_folder,"4co2_sw_x0.9452_offset/*_pa*.nc"),
                parallel=True,concat_dim="time")
        sw_minus=xr.open_mfdataset(os.path.join(input_folder,"ctl_solar50+_sw-_x0.95/*_pa*.nc"),
                parallel=True,concat_dim="time")        
        sw_plus=xr.open_mfdataset(os.path.join(input_folder,"ctl_solar50-_sw+_x1.052/*_pa*.nc"),
                parallel=True,concat_dim="time")
        return [fun(a) for a in (co2x4,solar,sw,sw_plus,sw_minus)]
                
def read_single_data(name):
        print(f"Process {os.getpid()} reading '{name}'")
        data = xr.open_mfdataset(os.path.join(input_folder,f"{name}/*_pa*.nc"),
                parallel=True,concat_dim="time")
        print(f"Process {os.getpid()} done reading '{name}'")        
        return fun(data)

@timer
def main():
        return [read_single_data(file) for file in files]

@timer
def main_parallel_mt():
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                result=executor.map(read_single_data,files)
        return result

@timer
def main_parallel_mp():
        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
                result=executor.map(read_single_data,files)
        return result

if __name__ == '__main__':        
        data0 = read_all_data()
        data1 = main()
        data2 = main_parallel_mt()
        data3 = main_parallel_mp()

        for i in range(4):
                print(f"Result of data{i} is:",eval(f"data{i}"))
