import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.cm as cm

nyears = 20
output_folder="/g/data/w40/dm5220/data/final_review_figures"
anomalies = lambda x,var: x[var] - ctl[var]
P = lambda x,var: x[var].t_student_probability(ctl[var])

# REPORT
ctl=my.UM.read_data('ctl')
co2x4=my.UM.read_data('4co2')
solar50p=my.UM.read_data('ctl_solar50+')
co2x4_fix=my.UM.read_data('4co2_fix_tsurf')
solar50p_fix=my.UM.read_data('ctl_fix_tsurf_solar50+')
co2x4_SWm=my.UM.read_data('4co2_sw-_x0.9452_offset')
co2x4_Solar50m=my.UM.read_data('4co2_solar50-')
solar50p_SWm=my.UM.read_data('ctl_solar50+_sw-_x0.9489_offset')

CO2_SOLAR=[co2x4, solar50p, co2x4_fix, solar50p_fix] 
CO2_SOLAR_titles=['4CO2', 'Solar50+', '4CO2 FIX TSURF', 'Solar50+ FIX TSURF']
CO2_SOLAR_colors=['darkred', 'mediumblue', 'red', 'turquoise']

SRM=[co2x4_Solar50m, co2x4_SWm, solar50p_SWm]
SRM_titles=['4CO2 Solar50-', '4CO2 SW-', 'Solar50+ SW-']
SRM_colors=['blueviolet','darkorange','forestgreen']

#====================================================#
#====================================================#
# FUNCTIONS

# PLOT COLORBAR 
def plot_cbar(var=None,cmap=None,
              levels=np.linspace(-2,2,50),
              du=None,label=None,
              outname=None):
    d=ctl[var].annual_mean()
    if len(d.dims) > 2: d=d.longitude_mean()
    d[0]=levels[0]-1
    d[1]=levels[-1]+1
    img=d.plotvar(levels=levels,
        cmap=cmap,
        add_colorbar=False,
        statistics=False)
    plt.clf()
    plt.colorbar(img,label=label,
                 ticks=np.arange(levels[0],levels[-1]+du,du),
                 extend='both',
                 ax=plt.axes())
    if outname is not None:
        plt.savefig(os.path.join(output_folder,outname),dpi=300,bbox_anchor='tight')
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
# PLOT AIR TEMPERATURE ABSOLUTE PROFILES
def plot_airprof(data,
    other_data=None,
    labels=None,
    colors=None,
    **kwargs):
    d=data['air_temperature_0_plev'].annual_mean(nyears*12).global_mean()
    if other_data is not None:
        od=[od['air_temperature_0_plev'].annual_mean(nyears*12).global_mean() for od in other_data]
    d=d.interp(pressure=np.linspace(50,800,1000),method='cubic')
    od=[x.interp(pressure=np.linspace(50,800,1000),method='cubic') for x in od]
    d.plotprof(
        other_data=od,
        colors=colors,
        labels=labels,
        units='$K$',
        lw=2,
        **kwargs)
    plt.legend()
    plt.title('Air Temperature Profiles')
def plot_airprof_zoom(data,
    labels=None,
    colors=None,
    other_data=None,
    **kwargs):
    d=data['air_temperature_0_plev'].annual_mean(nyears*12).global_mean()
    if other_data is not None:
        od=[od['air_temperature_0_plev'].annual_mean(nyears*12).global_mean() for od in other_data]
    d=d.interp(pressure=np.linspace(50,800,1000),method='cubic')
    od=[x.interp(pressure=np.linspace(50,800,1000),method='cubic') for x in od]
    d.plotprof(
        other_data=od,
        colors=colors,
        labels=labels,
        units='$K$',
        lw=2,
        **kwargs)
    plt.xlim((200,220))
    plt.ylim(200,50)
    plt.yticks([200,100,90,80,70,60,50],
              labels=[str(t) for t in [200,100,90,80,70,60,50]])
    plt.legend()
    plt.title('Air Temperature Profiles')
    plt.savefig(os.path.join(output_folder,'ABS_air_temp_profiles'),bbox_inches='tight',dpi=300)


#====================================================#
#====================================================#
### TIME SERIES

# TSURF Time series for CO2 Experiments
def plot():
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
    # plt.ylim(-0.25,1)
    plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.title('Surface Temperature | Time Series')
    plt.savefig(os.path.join(output_folder,'CO2_tsurf_tseries'),
                dpi=300,bbox_inches='tight')
plot()
# PRECIP Time series for CO2 Experiments
def plot():
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
    plt.ylim(-0.25,0.25)
    plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.title('Precipitation | Time Series')
    plt.savefig(os.path.join(output_folder,'CO2_precip_tseries'),
                dpi=300,bbox_inches='tight')
plot()
# OMEGA OVERTURNING Time series for CO2 Experiments
def plot():
    plt.figure()
    var='omega_overtuning'
    ma=15*12
    func=lambda x:x.sel(latitude_0=slice(-30,30))
    time_series(CO2_SOLAR[0],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[0],label=CO2_SOLAR_titles[0])
    time_series(CO2_SOLAR[1],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[1],label=CO2_SOLAR_titles[1])
    time_series(CO2_SOLAR[2],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[2],label=CO2_SOLAR_titles[2])
    time_series(CO2_SOLAR[3],var=var,moving_average=ma,
        func=func,color=CO2_SOLAR_colors[3],label=CO2_SOLAR_titles[3])
    plt.ylabel('[$m \cdot s^{-1}$]')
    # plt.ylim(-0.25,1)
    plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.title('Upward Air Velocity Overturning | Time Series')
    plt.savefig(os.path.join(output_folder,'CO2_overturning_tseries'),
                dpi=300,bbox_inches='tight')
plot()
# TSURF Time series for SRM Experiments
def plot():
    plt.figure()
    var='surface_temperature'
    ma=5*12
    time_series(SRM[0],var=var,moving_average=ma,
        color=SRM_colors[0],
        label=SRM_titles[0])
    time_series(SRM[1],var=var,moving_average=ma,
        color=SRM_colors[1],
        label=SRM_titles[1])
    time_series(SRM[2],var=var,moving_average=ma,
        color=SRM_colors[2],
        label=SRM_titles[2])
    time_series(CO2_SOLAR[-2],var=var,moving_average=ma,
        color=CO2_SOLAR_colors[-2],
        label=CO2_SOLAR_titles[-2])
    time_series(CO2_SOLAR[-1],var=var,moving_average=ma,
        color=CO2_SOLAR_colors[-1],
        label=CO2_SOLAR_titles[-1])
    plt.ylabel('[K]')
    plt.ylim(-1,1)
    plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.title('Surface Temperature | Time Series')
    plt.savefig(os.path.join(output_folder,'SRM_tsurf_tseries'),
                dpi=300,bbox_inches='tight')
plot()
# PRECIP Time series for SRM Experiments
def plot():
    plt.figure()
    var='precipitation_flux'
    ma=5*12
    func=lambda x: x.to_mm_per_day()
    time_series(SRM[0],var=var,moving_average=ma,
        func=func,
        color=SRM_colors[0],
        label=SRM_titles[0])
    time_series(SRM[1],var=var,moving_average=ma,
        func=func,
        color=SRM_colors[1],
        label=SRM_titles[1])
    time_series(SRM[2],var=var,moving_average=ma,
        func=func,
        color=SRM_colors[2],
        label=SRM_titles[2])
    time_series(CO2_SOLAR[-2],var=var,moving_average=ma,
        func=func,
        color=CO2_SOLAR_colors[-2],
        label=CO2_SOLAR_titles[-2])
    time_series(CO2_SOLAR[-1],var=var,moving_average=ma,
        func=func,
        color=CO2_SOLAR_colors[-1],
        label=CO2_SOLAR_titles[-1])
    plt.ylabel('[$mm \cdot d^{-1}$]')
    plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.title('Precipitation | Time Series')
    plt.savefig(os.path.join(output_folder,'SRM_precip_tseries'),
                dpi=300,bbox_inches='tight')
plot()
# OMEGA OVERTURNING Time series for SRM Experiments
def plot():
    plt.figure()
    var='omega_overtuning'
    ma=15*12
    func=lambda x:x.sel(latitude_0=slice(-30,30))
    time_series(SRM[0],var=var,moving_average=ma,
        func=func,color=SRM_colors[0],label=SRM_titles[0])
    time_series(SRM[1],var=var,moving_average=ma,
        func=func,color=SRM_colors[1],label=SRM_titles[1])
    time_series(SRM[2],var=var,moving_average=ma,
        func=func,color=SRM_colors[2],label=SRM_titles[2])
    time_series(CO2_SOLAR[-2],var=var,moving_average=ma,
        func=func,
        color=CO2_SOLAR_colors[-2],
        label=CO2_SOLAR_titles[-2])
    time_series(CO2_SOLAR[-1],var=var,moving_average=ma,
        func=func,
        color=CO2_SOLAR_colors[-1],
        label=CO2_SOLAR_titles[-1])
    plt.ylabel('[$m \cdot s^{-1}$]')
    plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.title('Upward Air Velocity Overturning | Time Series')
    plt.savefig(os.path.join(output_folder,'SRM_overturning_tseries'),
                dpi=300,bbox_inches='tight')
plot()
#====================================================#
#====================================================#
### TEMPERATURE PROFILES

# 4CO2 & SOLAR EXP
def plot():
    plt.figure()
    plot_airprof(data=ctl,other_data=CO2_SOLAR,
        colors=['black']+CO2_SOLAR_colors,
        labels=['Control']+CO2_SOLAR_titles)
    plt.xlim(150,300)
    plt.savefig(os.path.join(output_folder,'CO2_abs_tair_profiles'),
        dpi=300,bbox_inches='tight')
plot()
# 4CO2 & SOLAR EXP ZOOM
def plot():
    plt.figure()
    plot_airprof_zoom(data=ctl,other_data=CO2_SOLAR,
        colors=['black']+CO2_SOLAR_colors,
        labels=['Control']+CO2_SOLAR_titles)
    plt.savefig(os.path.join(output_folder,'CO2_abs_tair_profiles_ZOOM'),
        dpi=300,bbox_inches='tight')
plot()
# SRM EXP
def plot():
    plt.figure()
    plot_airprof(data=ctl,other_data=SRM+CO2_SOLAR[-2:],
        colors=['black']+SRM_colors+CO2_SOLAR_colors[-2:],
        labels=['Control']+SRM_titles+CO2_SOLAR_titles[-2:])
    plt.xlim(150,300)
    plt.savefig(os.path.join(output_folder,'SRM_abs_tair_profiles'),
        dpi=300,bbox_inches='tight')
plot()
# SRM EXP ZOOM
def plot():
    plt.figure()
    plot_airprof_zoom(data=ctl,other_data=SRM+CO2_SOLAR[-2:],
        colors=['black']+SRM_colors+CO2_SOLAR_colors[-2:],
        labels=['Control']+SRM_titles+CO2_SOLAR_titles[-2:])
    plt.savefig(os.path.join(output_folder,'SRM_abs_tair_profiles_ZOOM'),
        dpi=300,bbox_inches='tight')
plot()
# SRM EXP ZOOM + 4CO2 + SOLAR
def plot():
    plt.figure()
    plot_airprof_zoom(data=ctl,other_data=SRM+CO2_SOLAR[-2:]+[co2x4,solar50p],
        colors=['black']+SRM_colors+CO2_SOLAR_colors[-2:]+CO2_SOLAR_colors[:2],
        labels=['Control']+SRM_titles+CO2_SOLAR_titles[-2:]+CO2_SOLAR_titles[:2])
    plt.savefig(os.path.join(output_folder,'SRM_abs_tair_profiles_ZOOM_all'),
        dpi=300,bbox_inches='tight')
plot()

#====================================================#
#====================================================#
# CO2 EXP TAIR PROFILES
def plot():
    plt.figure()
    var='air_temperature_0_plev'
    data=[anomalies(x,var).global_mean().annual_mean(12*nyears) for x in CO2_SOLAR]
    data[0].plotprof(other_data=data[1:],
        double_axis=True,
        colors=CO2_SOLAR_colors,
        labels=CO2_SOLAR_titles,
        units='[K]',
        legend=True,
        legend_kwargs={'loc':'upper left',
            'bbox_to_anchor':(1.1,1.02)},
        title='Air Temperature Vertical Profiles')
    plt.savefig(os.path.join(output_folder,'CO2_tair_profiles'),
        dpi=300,bbox_inches='tight')
plot()

# SRM EXP TAIR PROFILES
def plot():
    plt.figure()
    var='air_temperature_0_plev'
    data=[anomalies(x,var).global_mean().annual_mean(12*nyears) for x in (SRM+[co2x4_fix,solar50p_fix])]
    data[0].plotprof(other_data=data[1:],
        double_axis=True,
        colors=SRM_colors+CO2_SOLAR_colors[-2:],
        labels=SRM_titles+CO2_SOLAR_titles[-2:],
        units='[K]',
        legend=True,
        legend_kwargs={'loc':'upper left',
            'bbox_to_anchor':(1.1,1.02)},
        title='Air Temperature Vertical Profiles')
    plt.savefig(os.path.join(output_folder,'SRM_tair_profiles'),
        dpi=300,bbox_inches='tight')
plot()
