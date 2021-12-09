import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os

input_folder = my.UM.data_folder
output_folder = "/g/data3/w48/dm5220/ancil/user_mlevel/tac_rad_change/files_for_xancil"
stream="c"
# stream="a"
alpha = 60*30 # K/s to K/30min
name = "mlev_ancil"
limit = 0.009
limit_lev=26

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

solar=read_data("4co2_solar50-")
sw=read_data("4co2_sw_x0.9452_offset")

def tot_hrates_anomalies(data):
    anomalies = lambda x,var: x[var] - ctl[var]
    var1="tendency_of_air_temperature_due_to_shortwave_heating"
    var2="tendency_of_air_temperature_due_to_longwave_heating"
    return anomalies(data,var1)+anomalies(data,var2)

# Total hrates in K/s
SW=tot_hrates_anomalies(sw)
SOLAR=tot_hrates_anomalies(solar)

SW.name = name
SOLAR.name = name

#Annual cycles in K/30min
swac=-SW.annual_cycle(20*360)*alpha
solarac=-SOLAR.annual_cycle(20*360)*alpha

# Correct values too big/small and set upper atmosphere corrections to 0
# swac=my.DataArray(swac.where(swac>=-limit,-limit).where(swac<=limit,limit))
# solarac=my.DataArray(solarac.where(solarac>=-limit,-limit).where(solarac<=limit,limit))

a=my.DataArray(swac.where(swac>100,0).where(np.logical_or(swac.model_level_number<7,swac.model_level_number>13),-0.007))
b=my.DataArray(swac.where(swac>100,0).where(np.logical_or(swac.model_level_number<7,swac.model_level_number>13),-0.008))
c=my.DataArray(swac.where(swac>100,0).where(np.logical_or(swac.model_level_number<7,swac.model_level_number>13),-0.009))
a.to_netcdf(os.path.join(output_folder,"tac_test_-0.007.nc"))
b.to_netcdf(os.path.join(output_folder,"tac_test_-0.008.nc"))
c.to_netcdf(os.path.join(output_folder,"tac_test_-0.009.nc"))

# # Convert to NetCDF
# swac.to_netcdf(os.path.join(output_folder,"tac_annual_4co2_sw-.nc"))
# solarac.to_netcdf(os.path.join(output_folder,"tac_annual_4co2_solar-.nc"))