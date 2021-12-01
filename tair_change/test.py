import myfuncs as my
import xarray as xr
from importlib import reload
import numpy as np
import os

input_folder = my.UM.data_folder
stream='c'
alpha = 60*60*24
name = "mlev_ancil"

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

# Total hrates in K/day
SW=tot_hrates_anomalies(sw)*alpha
SOLAR=tot_hrates_anomalies(solar)*alpha

SW.name = name
SOLAR.name = name
SW.to_netcdf("/g/data/w48/dm5220/scripts/tair_change/tac_all_4co2_sw-.nc",
            encoding={name: {"dtype": "int16", "zlib": True, "complevel":9}})
SOLAR.to_netcdf("/g/data/w48/dm5220/scripts/tair_change/tac_all_4co2_solar-.nc",
            encoding={name: {"dtype": "int16", "zlib": True, "complevel":9}})

#Annual cycles in K/day
swac=SW.annual_cycle()
solarac=SOLAR.annual_cycle()

swac.to_netcdf("/g/data/w48/dm5220/scripts/tair_change/tac_annual_4co2_sw-.nc",
            encoding={name: {"zlib": True, "complevel":8}})
solarac.to_netcdf("/g/data/w48/dm5220/scripts/tair_change/tac_annual_4co2_solar-.nc",
            encoding={name: {"zlib": True, "complevel":8}})