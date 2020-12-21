import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np


input_folder="/g/data/w48/dm5220/data"
var="air_temperature_0"
data_ctl = xr.open_mfdataset(os.path.join(input_folder,"control_new/vabva_pa*.nc"),
                  concat_dim="time",parallel=True)
data_4co2_fix_ctl = xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf_new/vabvc_pa*.nc"),
                  concat_dim="time",parallel=True)

sel = lambda x: x.isel(time=slice(0,10*12))
d=my.DataArray(sel(data_4co2_fix_ctl[var])-sel(data_ctl[var]))
ref=d.mean(["time","longitude"])



