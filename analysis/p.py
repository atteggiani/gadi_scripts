import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np

#%%
input_folder="/g/data/w48/dm5220/data/exp_precip_change"
alpha_precip=86400

data_ctl = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control/vabva_pa*.nc"),
           concat_dim="time",parallel=True))
data_test = my.add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"test/vabua_pa*.nc"),
           concat_dim="time",parallel=True))        
# %%
var="surface_temperature"
c=my.DataArray(data_ctl[var])
t=my.DataArray(data_test[var])
# %%
