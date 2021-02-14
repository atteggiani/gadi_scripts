import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np

input_folder="/g/data/w48/dm5220/data"

ctl=xr.open_mfdataset(os.path.join(input_folder,"tac_control/*_pc*.nc"),
        parallel=True,chunks={"time":50},concat_dim="time").surface_temperature                            

fix_tac=xr.open_mfdataset(os.path.join(input_folder,"4co2_fix_ctl_tac_nc/*_pc*.nc"),
           parallel=True,chunks={"time":50},concat_dim="time").surface_temperature                            

c=my.open_dataarray("/g/data/w48/dm5220/ancil/user_slevel/tair_change/files_for_xancil/tac_ctl.nc")

mask=np.tile((c!=0)[...,0],(144000,1,1))

# Annual cycle
c_ac=my.DataArray(c.where(c!=0,np.nan).groupby("time.dayofyear").mean("time").rename({"dayofyear":"time"})).transpose("time","latitude","longitude")
ctl_ac=my.DataArray(ctl.where(mask,np.nan).groupby("time.dayofyear").mean("time").rename({"dayofyear":"time"}))

# Annual cycle plot
plt.figure(); c_ac.mean(["longitude","latitude"]).plot()
plt.title("Annual cycle | prescribed tsurf")
plt.figure(); ctl_ac.mean(["longitude","latitude"]).plot()
plt.title("Annual cycle | control tsurf")

(c_ac.mean(["longitude","latitude"])-ctl_ac.mean(["longitude","latitude"])).plot()

# Annual mean difference plot
c.mean("time")
plt.figure(); my.DataArray(ctl_ac.mean("dayofyear")-c_ac.mean("dayofyear")).plotvar(title="Difference",cmap=my.Constants.colormaps.div_tsurf)

