import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import cartopy.crs as ccrs


input_folder="/g/data/w40/dm5220/data"
tac_folder="/g/data/w40/dm5220/ancil/user_mlevel/tair_change/sex"
output_folder="/g/data/w40/dm5220/data/figures/tac_sensitivity_experiments"

def get_tac_sex_filename(id):
    return os.readlink(os.path.join(tac_folder,id))

def open_tac_sex_file(id):
    folder=os.path.join(tac_folder,"files_for_xancil")
    return my.open_dataarray(os.path.join(folder,os.path.basename(get_tac_sex_filename(id)+".nc")))

def get_shape(id):
    lat=[int(x) for x in os.path.split(get_tac_sex_filename(id))[1].split(".")[1].split("_")]
    lev=[int(x) for x in os.path.split(get_tac_sex_filename(id))[1].split(".")[3].split("_")]
    return ((lat[0],lev[1]),lat[1]-lat[0],lev[0]-lev[1])

var="air_temperature"
data_ctl = xr.open_mfdataset(os.path.join(input_folder,"test/vabua_pa*.nc"),
                  concat_dim="time",parallel=True)
sel = lambda x: x.isel(time=slice(-10*12,None))
ctl=sel(data_ctl)
alphabet=list(map(chr,range(97,121)))
tac_sex_names=["sex{}".format(i+1) for i,_ in enumerate(alphabet)]

def plot_sex(id):
    ind=int(id[3:])-1
    try:
        data=sel(xr.open_mfdataset(os.path.join(input_folder,"tac_sensitivity_experiments/{}/vaby{}_pa*.nc".format(id,alphabet[ind])),concat_dim="time",parallel=True))
        p=my.DataArray(data[var].mean("longitude_0")).t_student_probability(ctl[var].mean("longitude_0"))
        d=my.DataArray(data[var].mean(["longitude_0","time"])-ctl[var].mean(["longitude_0","time"]))
    except:
        d=my.DataArray(ctl[var].where(False,0)).mean(["time","longitude_0"])
        p=False
    d.plotlev(levels=np.linspace(-3,3,50),
            cmap=my.Constants.colormaps.div_tsurf,
            cbar_kwargs={"ticks":np.arange(-3,3+0.5,0.5)},
            t_student=p)
    r=Rectangle(*get_shape(id),fill=False,ec="green",lw=1.5)
    plt.gca().add_patch(r)
    plt.title("Sensitivity experiment {}".format(id[3:]))
    plt.savefig(os.path.join(output_folder,"{}.png".format(id)),format='png',dpi=300,bbox_inches="tight")
    plt.show()

for id in tac_sex_names:
    plot_sex(id)