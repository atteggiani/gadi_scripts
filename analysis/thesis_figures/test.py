import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.gridspec import GridSpec

nyears = 20
output_folder="/g/data/w40/dm5220/data/thesis_figures"
anomalies = lambda x,var: my.DataArray(x[var] - ctl[var])
P = lambda x,var: x[var].t_student_probability(ctl[var])

# DATA
ctl=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl.nc")
co2x4=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2.nc")
solar50p=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_solar50+.nc")
co2x4_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2_fix_tsurf.nc")
solar50p_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_fix_tsurf_solar50+.nc")

CO2_SOLAR=[co2x4, solar50p, co2x4_fix, solar50p_fix] 
CO2_SOLAR_titles=['4CO2', 'Solar50+', '4CO2 FIX TSURF', 'Solar50+ FIX TSURF']
CO2_SOLAR_colors=['darkred', 'mediumblue', 'red', 'turquoise']

#====================================================#
#====================================================#
# PLOT TIME SERIES
def time_series(data,var="surface_temperature",
                func=lambda x: x,
                moving_average=60,
                title=None,
                **kwargs):
    d=func(anomalies(data,var))
    if 'pressure' in d.dims:
        d=d.sel({"pressure":500},method="nearest")
    tseries=d.global_mean()
    if moving_average is not None:
        tseries=tseries.rolling(time=moving_average, center=True, min_periods=2).mean()
    def fun(x):
        n=len(x.time)
        x2=x.isel(time=slice(-12*nyears,None))
        x1=x.isel(time=slice(0,n-(nyears*12))) 
        x2.plot(**kwargs)
        kwargs["label"]=None
        x1.plot(**kwargs,linestyle="-.",linewidth=0.8)
        gm=x2.mean() 
        c = kwargs.pop("color") if "color" in kwargs else None 
        plt.axhline(y = gm, color=c, **kwargs,linestyle = '-.',linewidth=0.5) 
        plt.axhline(y = 0, color = 'k', linestyle = '-',linewidth=0.5) 
        plt.title(title)
        plt.xlabel("Years")
        plt.gca().set_xticks(np.arange(0,n+12*5,12*5))
        plt.gca().set_xticklabels(np.arange(0,n/12+5,5,dtype=int))
        plt.grid(color='grey',linestyle='--')
    fun(tseries.assign_coords({"time":np.arange(1,len(tseries.time)+1)}))

# TSURF Time series 
def tsurf_tseries():
    plt.figure()
    var='surface_temperature'
    ma=5*12
    time_series(CO2_SOLAR[0],var=var,moving_average=ma,
        color=CO2_SOLAR_colors[0],label=CO2_SOLAR_titles[0])
    time_series(CO2_SOLAR[1],var=var,moving_average=ma,
        color=CO2_SOLAR_colors[1],label=CO2_SOLAR_titles[1])
    time_series(CO2_SOLAR[2],var=var,moving_average=ma,
        color=CO2_SOLAR_colors[2],label=CO2_SOLAR_titles[2])
    time_series(CO2_SOLAR[3],var=var,moving_average=ma,
        color=CO2_SOLAR_colors[3],label=CO2_SOLAR_titles[3])
    plt.ylabel('[K]')
    plt.xlabel('Year of simulation')
    # plt.ylim(-0.25,1)
    # plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.legend()
    plt.title('Surface Temperature Anomalies | Time Series')
    plt.savefig(os.path.join(output_folder,'CO2_tsurf_tseries'),
                dpi=300,bbox_inches='tight')
tsurf_tseries()

# PRECIP Time series 
def precip_tseries():
    plt.figure()
    var='precipitation_flux'
    ma=5*12
    func=lambda x: x.to_mm_per_day()
    time_series(CO2_SOLAR[0],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[0],label=CO2_SOLAR_titles[0])
    time_series(CO2_SOLAR[1],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[1],label=CO2_SOLAR_titles[1])
    time_series(CO2_SOLAR[2],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[2],label=CO2_SOLAR_titles[2])
    time_series(CO2_SOLAR[3],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[3],label=CO2_SOLAR_titles[3])
    plt.ylabel('[$mm \cdot d^{-1}]$')
    plt.xlabel('Year of simulation')
    plt.ylim(-0.25,0.25)
    # plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.legend()
    plt.title('Precipitation Anomalies | Time Series')
    plt.savefig(os.path.join(output_folder,'CO2_precip_tseries'),
                dpi=300,bbox_inches='tight')
precip_tseries()
