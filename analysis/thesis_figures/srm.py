import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import string

nyears = 20
output_folder="/g/data/w40/dm5220/data/thesis_figures"

# DATA
ctl=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl.nc")
co2x4_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2_fix_tsurf.nc")
solar50p_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_fix_tsurf_solar50+.nc")
co2x4solar50m=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2_solar50-.nc")
co2x4SWm=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2_sw-.nc")
solar50mSWp=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_solar50+_sw-.nc")

SRM=[co2x4_fix, solar50p_fix, co2x4solar50m, co2x4SWm, solar50mSWp] 
SRM_titles=['4CO2 FIX TSURF', 'Solar50+ FIX TSURF','4CO2 Solar50-','4CO2 SW-','Solar50+ SW-']
SRM_colors=['red', 'turquoise', 'orange', 'purple', 'green']
seasons=["DJF","MAM","JJA","SON"]
axes_labels=[f"({l})" for l in list(string.ascii_lowercase)]

def anomalies(x,var,ctrl=ctl,func=lambda x: x):
     return my.DataArray(x[var] - ctrl[var])
P = lambda x,var: my.DataArray(x[var]).t_student_probability(my.DataArray(ctl[var]),num_years=nyears)
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

def plot_vert(data,mean="lon",var="air_temperature_0_plev",
    func=lambda x: x, ctrl=ctl, **kwargs):
    if mean == "lon":
        fmean=lambda x: x.longitude_mean()
    else:
        fmean=lambda x: x.latitude_mean()
    t=fmean(P(data,var))
    kwargs.setdefault("t_student",t)
    d=func(anomalies(data,var,ctrl=ctrl))
    
    im=fmean(d.annual_mean(12*nyears)).plotlev(**kwargs)
    return im

# TSURF ANOMALIES
def tsurf_anom():
    grid = GridSpec(3,4,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.5,hspace=0.10)
    gridcb = GridSpec(1, 4,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.2),3))
    axes=[fig.add_subplot(grid[0,:2],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[0,2:],projection=ccrs.PlateCarree())] +\
         [fig.add_subplot(grid[1,:2],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[1,2:],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[2,1:3],projection=ccrs.PlateCarree()),] +\
         [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Surface Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        title="",
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        statistics={'value':'all','fontsize':11,"position":(0.5,-0.15)},
        extend='both',
        )
    for i in range(5):
    # plot 1
        im=plot_anom(SRM[i],
            ax=axes[i],
            **kwargs,
            )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-3,3+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'SRM_tsurf_anom'),
                dpi=300,bbox_inches='tight')
tsurf_anom()

def tsurf_anom_season():
    grid = GridSpec(5,4,
            left=0.05, right=0.95, top=0.93, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(4) for j in range(4)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Surface Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        statistics={'value':'all','fontsize':8,"position":(0.5,-0.15)},
        extend='both',
        grid=False,
        )
    # plots
    axit=iter(axes)
    for i,_ in enumerate(SRM):
        for season in seasons:
            ax=next(axit)
            im=plot_anom(SRM[i],
                ax=ax,
                func= lambda x: x.group_by("season",num=12*nyears).sel(time=season),
                title=season,
                **kwargs,
                )
            if i > 0:
                ax.set_title("")        
    
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-3,3+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'SRM_tsurf_anom_season'),
                dpi=300,bbox_inches='tight')
tsurf_anom_season()

# PRECIP ANOMALIES
def precip_anom():
    grid = GridSpec(3,4,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.5,hspace=0.10)
    gridcb = GridSpec(1, 4,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.2),3))
    axes=[fig.add_subplot(grid[0,:2],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[0,2:],projection=ccrs.PlateCarree())] +\
         [fig.add_subplot(grid[1,:2],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[1,2:],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[2,1:3],projection=ccrs.PlateCarree()),] +\
         [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation Change",fontsize=16)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-2,2,20),
        du=0.25,
        title="",
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        statistics={'value':'all','fontsize':11,"position":(0.5,-0.15)},
        )
    for i in range(5):
    # plot 1
        im=plot_anom(SRM[i],
            ax=axes[i],
            **kwargs,
            )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-2,2+0.25,0.25),
        )   
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'SRM_precip_anom'),
                dpi=300,bbox_inches='tight')
precip_anom()

# TAIR ANOMALIES
def tair_anom():
    grid = GridSpec(3,4,
            left=0.05, right=0.95, top=0.91, bottom=0.13,
            wspace=1.2,hspace=0.3)
    gridcb = GridSpec(1, 4,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ============== LONGMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.5),3))
    axes=[fig.add_subplot(grid[0,:2]),
          fig.add_subplot(grid[0,2:])] +\
         [fig.add_subplot(grid[1,:2]),
          fig.add_subplot(grid[1,2:]),
          fig.add_subplot(grid[2,1:3]),] +\
         [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        title="",
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        double_axis=True,
        extend='both',
        )
    for i in range(5):
    # plot 1
        im=plot_vert(SRM[i],
            ax=axes[i],
            **kwargs,
            )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-3,3+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'SRM_tair_anom_lonmean'),
                dpi=300,bbox_inches='tight')
    return
    # ============== LATMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[0,:2]),
          fig.add_subplot(grid[0,2:])] +\
         [fig.add_subplot(grid[1,:2]),
          fig.add_subplot(grid[1,2:]),
          fig.add_subplot(grid[2,1:3]),] +\
         [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        title="",
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        double_axis=True,
        extend='both',
        mean="lat",
        )
    for i in range(5):
    # plot 1
        im=plot_vert(SRM[i],
            ax=axes[i],
            **kwargs,
            )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-3,3+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'SRM_tair_anom_latmean'),
                dpi=300,bbox_inches='tight')
tair_anom()

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
    for i,_ in enumerate(SRM):
        time_series(SRM[i],var=var,moving_average=ma,
            color=SRM_colors[i],label=SRM_titles[i])
    plt.ylabel('[K]')
    plt.xlabel('Year of simulation')
    # plt.ylim(-0.2,0.1)
    # plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.legend()
    plt.title('Surface Temperature Change')
    plt.savefig(os.path.join(output_folder,'SRM_tsurf_tseries'),
                dpi=300,bbox_inches='tight')
tsurf_tseries()

# PRECIP Time series 
def precip_tseries():
    plt.figure()
    var='precipitation_flux'
    ma=5*12
    func=lambda x: x.to_mm_per_day()
    for i,_ in enumerate(SRM):
        time_series(SRM[i],var=var,moving_average=ma,
            func=func,color=SRM_colors[i],label=SRM_titles[i])
    plt.ylabel('[$mm \cdot d^{-1}]$')
    plt.xlabel('Year of simulation')
    plt.ylim(-0.25,0.12)
    # plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.legend()
    plt.title('Precipitation Change')
    plt.savefig(os.path.join(output_folder,'SRM_precip_tseries'),
                dpi=300,bbox_inches='tight')
precip_tseries()

#====================================================#
#====================================================#
# PLOT TAIR ABSOLUTE PROFILES
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
    plot_airprof(data=ctl,other_data=SRM,
            colors=['black']+SRM_colors,
            labels=['Control']+SRM_titles,
            double_axis=True,
            legend=False,
            ax=axm,
            title="")
    axm.set_xlim(150,300)
    # Zoom Plot
    plot_airprof(ax=axz,data=ctl,other_data=SRM,
            colors=['black']+SRM_colors,
            labels=['Control']+SRM_titles,
            double_axis=False,
            title="")
    axz.set_xlim((200,220))
    axz.set_ylim(200,50)
    axz.set_yticks([200,100,90,80,70,60,50])
    axz.set_yticklabels([str(t) for t in [200,100,90,80,70,60,50]])
    # Add min
    v=[line.get_ydata()[np.argmin(line.get_xdata())] for line in axz.get_lines()]
    axz.hlines(v, *axz.get_xlim(), colors=["black"]+SRM_colors, linestyles='dashed', label='',linewidth=0.75)

    # Add zoom effect
    my.zoom_effect(axm,axz,xlim=(200,220),ylim=(200,50),
        patch1_kwargs=dict(edgecolor="red",fill=True,facecolor=[0,0,1,0.1],ls="--"),
        patch2_kwargs=dict(edgecolor="none",fill=False),
        lines_kwargs=dict(color="red",ls="--"))
    # Label subplots
    axm.set_title("(a)", fontfamily='serif', loc='left', fontsize='large')
    axz.set_title("(b)", fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'SRM_abs_airprof'),
                dpi=300,bbox_inches='tight')
air_prof_zoom()

# PLOT TAIR CHANGE PROFILES
def air_prof_anom():
    plt.figure()
    var='air_temperature_0_plev'
    data=[anomalies(x,var).global_mean().annual_mean(12*nyears) for x in SRM]
    data[0].plotprof(other_data=data[1:],
        double_axis=True,
        colors=SRM_colors,
        labels=SRM_titles,
        units='[K]',
        legend=True,
        # legend_kwargs={'loc':'upper left',
        #     'bbox_to_anchor':(1.1,1.02)},
        title='Air Temperature Change')
    plt.savefig(os.path.join(output_folder,'SRM_anom_airprof'),
        dpi=300,bbox_inches='tight')
air_prof_anom()

#====================================================#