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
from decorators import timed
from metpy.interpolate import log_interpolate_1d
from metpy.units import units
from scipy.interpolate import interp1d
import matplotlib.colors as colors
from importlib import reload

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

input_folder = "/g/data/w48/dm5220/data"
d=read_data(input_folder,["ctl"])[0]
