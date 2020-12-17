import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np


input_folder="/g/data/w48/dm5220/data/exp_precip_change"
var="air_temperature"
data_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control/vabva_pa*.nc"),
                  concat_dim="time",parallel=True))[var]
data_4co2_fix_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/vabvc_pa*.nc"),
                  concat_dim="time",parallel=True))[var]



