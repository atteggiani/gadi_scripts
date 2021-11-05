import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
# import os
# import matplotlib.pyplot as plt

# import matplotlib.colors as colors
# from gc import collect
# import concurrent.futures
# import dask
# from dask.diagnostics import ProgressBar
# from decorators import timed
# from metpy.interpolate import log_interpolate_1d
# from metpy.units import units
# from scipy.interpolate import interp1d
# import matplotlib.colors as colors

input_folder = my.UM.data_folder
stream='c'

def read_data(folder):
    return my.open_mfdataset(
        os.path.join(input_folder,f"{folder}/*_p{stream}*.nc"),
        parallel=True,
        combine="nested",
        concat_dim="time",
        compat='override',
        coords='minimal',
        )

ctl=read_data("ctl")

def tot_hrates_anomalies(data):
    swhr="tendency_of_air_temperature_due_to_shortwave_heating"
    lwhr="tendency_of_air_temperature_due_to_longwave_heating"
    return data[swhr]+data[lwhr] - ctl[swhr]+ctl[lwhr]

solar=read_data("4co2_solar50-")
sw=read_data("4co2_sw_x0.9452_offset")

# Total hrates
SW=tot_hrates_anomalies(sw)
SOLAR=tot_hrates_anomalies(solar)
