import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np

a=my.open_dataarray("/g/data/w48/dm5220/ancil/user_slevel/tair_change/files_for_xancil/tac_ctl.nc")
corr=0.0001
a+=corr
output_file="/g/data/w48/dm5220/ancil/user_slevel/tair_change/files_for_xancil/tac_ctl_corr_{}.nc".format(corr)
encoding = {a.name: {'zlib':True,'shuffle':True,'complevel':4}}
a.to_netcdf(output_file,encoding=encoding)