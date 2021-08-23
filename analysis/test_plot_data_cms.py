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
files = ["ctl","4co2","4co2_solar50-","4co2_sw_x0.9452_offset","ctl_solar50+_sw-_x0.95","ctl_solar50-_sw+_x1.052"]

def read_single_data(input_folder,name):
    print(f"Process {os.getpid()} reading '{name}'")
    data = xr.open_mfdataset(os.path.join(input_folder,f"{name}/*_pa*.nc"),
            parallel=True,concat_dim="time")
    print(f"Process {os.getpid()} done reading '{name}'")        
    return data

# def read_all_data():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
#             result=executor.map(read_single_data,names)
#     return result

all_data = {file:read_single_data(input_folder,file) for file in files}

def plot_annual_mean(file,data_variable):
    print(f"Process {os.getpid()} plotting '{data_variable}' of '{file}'")
    data = all_data[file][data_variable]
    im=data.mean(["latitude","longitude"]).plot()
    print(f"Process {os.getpid()} done plotting '{data_variable}' of '{file}'")
    return im

@timer
def main():
    [plot_annual_mean(file,"surface_temperature") for file in files]

@timer
def main_parallel_mt():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(lambda x: plot_annual_mean(x,"surface_temperature"),files)

@timer
def main_parallel_mp():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(lambda x: plot_annual_mean(x,"surface_temperature"),files)

if __name__ == "__main__":
    main()
    main_parallel_mt()
    main_parallel_mp()
