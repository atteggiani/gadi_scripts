import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import matplotlib.cm as cm

nyears = 20
output_folder="/g/data/w40/dm5220/data/thesis_figures"

# DATA
ctl=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl.nc")
co2x4=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2.nc")
solar50p=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_solar50+.nc")
co2x4_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2_fix_tsurf.nc")
solar50p_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_fix_tsurf_solar50+.nc")

CO2_SOLAR=[co2x4, solar50p, co2x4_fix, solar50p_fix] 
CO2_SOLAR_titles=['4CO2', 'Solar50+', '4CO2 FIX TSURF', 'Solar50+ FIX TSURF']
CO2_SOLAR_colors=['darkred', 'mediumblue', 'red', 'turquoise']

def anomalies(x,var,ctrl=ctl):
     return my.DataArray(x[var] - ctrl[var])
P = lambda x,var: my.DataArray(x[var]).t_student_probability(my.DataArray(ctl[var]))
#====================================================#
#====================================================#
# ANOMALIES
def plot_anom(data,var="surface_temperature",
    func=lambda x: x, ctrl=ctl, **kwargs):
    t=P(data,var)
    kwargs.setdefault("t_student",t)
    d=func(anomalies(data,var,ctrl=ctrl))
    im=d.annual_mean(12*nyears).plotvar(**kwargs)
    return im

# TSURF ANOMALIES
def tsurf_anom():
    grid = GridSpec(2,3,
            left=0.05, right=0.95, top=0.9, bottom=0.2,
            wspace=0.12,hspace=0.1)
    gridcb = GridSpec(1, 3,
            left=0.05, right=0.95, top=0.1, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((4,1.9),3))
    fig.suptitle("Surface Temperature Change",fontsize=16)
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(2) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        units="K",
        title="",
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        statistics={'value':'all','fontsize':11,"position":(0.5,-0.15)},
        )
    # plot 1
    plot_anom(CO2_SOLAR[0],
        ax=axes[0],
        **kwargs,
        )
    # plot 2
    plot_anom(CO2_SOLAR[1],
        ax=axes[1],
        **kwargs,
        )
    # plot 3
    plot_anom(CO2_SOLAR[1],
        ctrl=CO2_SOLAR[0],
        ax=axes[2],
        t_student=False,
        **kwargs,
        )
    # plot 4
    plot_anom(CO2_SOLAR[2],
        ax=axes[3],
        **kwargs,
        )
    # plot 5
    plot_anom(CO2_SOLAR[3],
        ax=axes[4],
        **kwargs,
        )
    # plot 6
    im=plot_anom(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[2],
        ax=axes[5],
        t_student=False,
        extend='both',
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="K",
        ticks=np.arange(-3,3+0.5,0.5),
        )
tsurf_anom()

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


#====================================================#
#====================================================#
# PLOT AIR TEMPERATURE ABSOLUTE PROFILES
def plot_airprof(data,
    other_data=None,
    labels=None,
    colors=None,
    **kwargs):
    d=my.DataArray(data['air_temperature_0_plev']).annual_mean(nyears*12).global_mean()
    if other_data is not None:
        od=[my.DataArray(od['air_temperature_0_plev']).annual_mean(nyears*12).global_mean() for od in other_data]
    d=d.interp(pressure=np.linspace(50,800,1000),method='cubic')
    od=[x.interp(pressure=np.linspace(50,800,1000),method='cubic') for x in od]
    d.plotprof(
        other_data=od,
        colors=colors,
        labels=labels,
        units='$K$',
        lw=2,
        **kwargs)

def air_prof_zoom():
    grid = GridSpec(4, 5,
        left=0.05, bottom=0.05, right=0.95, top=0.88,
        wspace=2)
    fig = plt.figure(figsize=np.multiply((5,3),1.7))
    fig.suptitle("Air Temperature",fontsize=16)
    axm = fig.add_subplot(grid[1:3,0:2])
    axz = fig.add_subplot(grid[:,2:])
    # Main Plot
    plot_airprof(data=ctl,other_data=CO2_SOLAR,
            colors=['black']+CO2_SOLAR_colors,
            labels=['Control']+CO2_SOLAR_titles,
            double_axis=True,
            legend=False,
            ax=axm,
            title="")
    axm.set_xlim(150,300)
    # Zoom Plot
    plot_airprof(ax=axz,data=ctl,other_data=CO2_SOLAR,
            colors=['black']+CO2_SOLAR_colors,
            labels=['Control']+CO2_SOLAR_titles,
            double_axis=True,
            title="")
    axz.set_xlim((200,220))
    axz.set_ylim(200,50)
    axz.set_yticks([200,100,90,80,70,60,50])
    axz.set_yticklabels([str(t) for t in [200,100,90,80,70,60,50]])
    # Add min
    v=[line.get_ydata()[np.argmin(line.get_xdata())] for line in axz.get_lines()]
    axz.hlines(v, *axz.get_xlim(), colors=["black"]+CO2_SOLAR_colors, linestyles='dashed', label='',linewidth=0.75)

    # Add zoom effect
    my.zoom_effect(axm,axz,xlim=(200,220),ylim=(200,50),
        patch1_kwargs=dict(edgecolor="red",fill=True,facecolor=[0,0,1,0.1],ls="--"),
        patch2_kwargs=dict(edgecolor="none",fill=False),
        lines_kwargs=dict(color="red",ls="--"))
    # Label subplots
    axm.set_title("(a)", fontfamily='serif', loc='left', fontsize='large')
    axz.set_title("(b)", fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_abs_airprof'),
                dpi=300,bbox_inches='tight')
air_prof_zoom()

# CO2 EXP TAIR PROFILES
def air_prof_anom():
    plt.figure()
    var='air_temperature_0_plev'
    data=[anomalies(x,var).global_mean().annual_mean(12*nyears) for x in CO2_SOLAR]
    data[0].plotprof(other_data=data[1:],
        double_axis=True,
        colors=CO2_SOLAR_colors,
        labels=CO2_SOLAR_titles,
        units='[K]',
        legend=True,
        # legend_kwargs={'loc':'upper left',
        #     'bbox_to_anchor':(1.1,1.02)},
        title='Air Temperature Anomalies')
    plt.savefig(os.path.join(output_folder,'CO2_anom_airprof'),
        dpi=300,bbox_inches='tight')
air_prof_anom()

#====================================================#
    
# # OMEGA OVERTURNING Time series for CO2 Experiments
# def plot():
#     plt.figure()
#     var='omega_overtuning'
#     ma=15*12
#     func=lambda x:x.sel(latitude_0=slice(-30,30))
#     time_series(CO2_SOLAR[0],var=var,moving_average=ma,
#         func=func,color=CO2_SOLAR_colors[0],label=CO2_SOLAR_titles[0])
#     time_series(CO2_SOLAR[1],var=var,moving_average=ma,
#         func=func,color=CO2_SOLAR_colors[1],label=CO2_SOLAR_titles[1])
#     time_series(CO2_SOLAR[2],var=var,moving_average=ma,
#         func=func,color=CO2_SOLAR_colors[2],label=CO2_SOLAR_titles[2])
#     time_series(CO2_SOLAR[3],var=var,moving_average=ma,
#         func=func,color=CO2_SOLAR_colors[3],label=CO2_SOLAR_titles[3])
#     plt.ylabel('[$m \cdot s^{-1}$]')
#     # plt.ylim(-0.25,1)
#     plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
#     plt.title('Upward Air Velocity Overturning | Time Series')
#     plt.savefig(os.path.join(output_folder,'CO2_overturning_tseries'),
#                 dpi=300,bbox_inches='tight')
# plot()


#====================================================#
#====================================================#
