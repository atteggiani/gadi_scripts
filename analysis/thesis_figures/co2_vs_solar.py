import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import string

nyears = 20
output_folder="/g/data/w40/dm5220/data/thesis_figures/ch3"

# DATA
ctl=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl.nc")
co2x4=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2.nc")
solar50p=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_solar50+.nc")
co2x4_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/4co2_fix_tsurf.nc")
solar50p_fix=xr.open_dataset("/g/data/w40/dm5220/data/processed_data/ctl_fix_tsurf_solar50+.nc")

CO2_SOLAR=[co2x4, co2x4_fix, solar50p, solar50p_fix]
CO2_SOLAR_titles=['4CO2', '4CO2 FIX TSURF', 'Solar50+', 'Solar50+ FIX TSURF']
CO2_SOLAR_colors=['darkred', 'red', 'mediumblue', 'turquoise']
seasons=["DJF","MAM","JJA","SON"]
axes_labels=[f"({l})" for l in list(string.ascii_lowercase)]
def anomalies(x,var,ctrl=ctl):
     return my.DataArray(x[var] - ctrl[var])
def P(x,var,ctrl=ctl):
     return my.DataArray(x[var]).t_student_probability(my.DataArray(ctrl[var]),num_years=nyears)
def rad_forcing(x,ctrl=ctl):
    rad = lambda x: x["toa_incoming_shortwave_flux"] - (x["toa_outgoing_longwave_flux"] + x["toa_outgoing_shortwave_flux"])  
    return my.DataArray(rad(x) - rad(ctrl))
#====================================================#
#====================================================#
# ANOMALIES
def plot_anom(data,var="surface_temperature",
    func=lambda x: x, ctrl=ctl, analysis='amean', **kwargs):
    d=func(anomalies(data,var,ctrl=ctrl))
    if analysis == 'amean':
        t=P(data,var)
        kwargs.setdefault("t_student",t)
        im=d.annual_mean(12*nyears).plotvar(**kwargs)
    elif analysis == 'seascyc':
        im=d.seasonal_cycle(12*nyears).plotvar(**kwargs)
    else:
        raise Exception("Type of analysis not understood")
    return im

def plot_vert(data,mean="lon",var="air_temperature_0_plev",
    func=lambda x: x, ctrl=ctl, analysis='amean', **kwargs):
    if mean == "lon":
        fmean=lambda x: x.longitude_mean()
    else:
        fmean=lambda x: x.latitude_mean()
    d=func(anomalies(data,var,ctrl=ctrl))
    if analysis == 'amean':
        t=fmean(P(data,var))
        kwargs.setdefault("t_student",t)
        im=fmean(d.annual_mean(12*nyears)).plotlev(**kwargs)
    elif analysis == 'seascyc':
        im=fmean(d.seasonal_cycle(12*nyears)).plotlev(**kwargs)
    else:
        raise Exception("Type of analysis not understood")
    
    return im

# TSURF ANOMALIES

def tsurf_anom():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Surface Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        statistics={'value':'all','fontsize':11,"position":(0.5,-0.15)},
        extend='both',
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_anom(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            **kwargs,
            )
    # plot 5
    plot_anom(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        **kwargs,
        )
    # plot 6
    im=plot_anom(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        title=f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
        t_student=False,
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
    plt.savefig(os.path.join(output_folder,'CO2_tsurf_anom'),
                dpi=300,bbox_inches='tight')
tsurf_anom()

def tsurf_anom_seascyc():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Surface Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-2,2,20),
        du=0.5,
        cmap=my.Colormaps.div_precip_r,
        add_colorbar=False,
        statistics={'value':'rms','fontsize':11,"position":(0.5,-0.15)},
        extend='both',
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_anom(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            analysis='seascyc',
            **kwargs,
            )
    # plot 5
    plot_anom(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot 6
    im=plot_anom(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        title=f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
        ax=axes[5],
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-2,2+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_tsurf_anom_seascyc'),
                dpi=300,bbox_inches='tight')
tsurf_anom_seascyc()

def tsurf_anom_season():
    grid = GridSpec(4,4,
            left=0.05, right=0.95, top=0.93, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,2.5),3))
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
    for i,_ in enumerate(CO2_SOLAR):
        for season in seasons:
            ax=next(axit)
            im=plot_anom(CO2_SOLAR[i],
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
    plt.savefig(os.path.join(output_folder,'CO2_tsurf_anom_season'),
                dpi=300,bbox_inches='tight')
tsurf_anom_season()

# PRECIP ANOMALIES
def precip_anom():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation Change",fontsize=16)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-2,2,20),
        du=0.5,
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        statistics={'value':'all','fontsize':11,"position":(0.5,-0.15)},
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_anom(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            **kwargs,
            )
    # plot 5
    plot_anom(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        **kwargs,
        )
    # plot 6
    im=plot_anom(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        title=f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
        t_student=False,
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-2,2+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_precip_anom'),
                dpi=300,bbox_inches='tight')
precip_anom()

def precip_anom_seascyc():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation Change",fontsize=16)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-2,2,20),
        du=0.5,
        cmap=my.Colormaps.div_precip_r,
        add_colorbar=False,
        extend='both',
        statistics={'value':'rms','fontsize':11,"position":(0.5,-0.15)},
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_anom(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            analysis='seascyc',
            **kwargs,
            )
    # plot 5
    plot_anom(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot 6
    im=plot_anom(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        title=f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-2,2+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_precip_anom_seascyc'),
                dpi=300,bbox_inches='tight')
precip_anom_seascyc()

def precip_anom_season():
    grid = GridSpec(4,4,
            left=0.05, right=0.95, top=0.93, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,2.5),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(4) for j in range(4)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation Change",fontsize=16)
    kwargs=dict(
        var="precipitation_flux",
        levels=np.linspace(-2,2,20),
        du=0.5,
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        statistics={'value':'all','fontsize':8,"position":(0.5,-0.15)},
        grid=False,
        )
    # plots
    axit=iter(axes)
    for i,_ in enumerate(CO2_SOLAR):
        for season in seasons:
            ax=next(axit)
            im=plot_anom(CO2_SOLAR[i],
                ax=ax,
                func=lambda x: x.group_by("season",num=12*nyears).sel(time=season).to_mm_per_day(),
                title=season,
                **kwargs,
                )
            if i > 0:
                ax.set_title("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-2,2+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_precip_anom_season'),
                dpi=300,bbox_inches='tight')
precip_anom_season()

# TAIR ANOMALIES
def tair_anom():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.91, bottom=0.13,
            wspace=0.43,hspace=0.3)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ============== LONGMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        double_axis="height",
        extend='both',
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_vert(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            **kwargs,
            )
    # plot 5
    plot_vert(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        **kwargs,
        )
    # plot 6
    im=plot_vert(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        title={"label":f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
               "fontsize":10},
        t_student=False,
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
    plt.savefig(os.path.join(output_folder,'CO2_tair_anom_lonmean'),
                dpi=300,bbox_inches='tight')
    
    # ============== LATMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        double_axis="height",
        extend='both',
        mean="lat",
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_vert(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            **kwargs,
            )
    # plot 5
    plot_vert(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        **kwargs,
        )
    # plot 6
    im=plot_vert(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        title={"label":f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
               "fontsize":10},
        t_student=False,
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
    plt.savefig(os.path.join(output_folder,'CO2_tair_anom_latmean'),
                dpi=300,bbox_inches='tight')
tair_anom()

def tair_anom_seascyc():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.91, bottom=0.13,
            wspace=0.43,hspace=0.3)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ============== LONGMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-2,2,20),
        du=0.5,
        cmap=my.Colormaps.div_precip_r,
        add_colorbar=False,
        double_axis="height",
        extend='both',
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_vert(CO2_SOLAR[i],
            ax=axes[i],
            title=CO2_SOLAR_titles[i],
            analysis='seascyc',
            **kwargs,
            )
    # plot 5
    plot_vert(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        title=f"{CO2_SOLAR_titles[2]} - {CO2_SOLAR_titles[0]}",
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot 6
    im=plot_vert(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        title=f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-2,2+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_tair_anom_lonmean_seascyc'),
                dpi=300,bbox_inches='tight')
                
    # ============== LATMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-2,2,20),
        du=0.5,
        title="",
        cmap=my.Colormaps.div_precip_r,
        add_colorbar=False,
        double_axis="height",
        extend='both',
        mean="lat",
        )
    # plots
    for i,_ in enumerate(CO2_SOLAR):
        plot_vert(CO2_SOLAR[i],
            ax=axes[i],
            analysis='seascyc',
            **kwargs,
            )
    # plot 5
    plot_vert(CO2_SOLAR[2],
        ctrl=CO2_SOLAR[0],
        ax=axes[4],
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot 6
    im=plot_vert(CO2_SOLAR[3],
        ctrl=CO2_SOLAR[1],
        ax=axes[5],
        t_student=False,
        analysis='seascyc',
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-2,2+0.5,0.5),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'CO2_tair_anom_latmean_seascyc'),
                dpi=300,bbox_inches='tight')
tair_anom_seascyc()

def tair_anom_season():
    grid = GridSpec(4,4,
            left=0.05, right=0.95, top=0.93, bottom=0.12,
            wspace=0.17,hspace=0.2)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ============== LONGMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.5),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(4) for j in range(4)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        extend='both',
        )
    # plots
    axit=iter(axes)
    for i,_ in enumerate(CO2_SOLAR):
        for season in seasons:
            ax=next(axit)
            im=plot_vert(CO2_SOLAR[i],
                ax=ax,
                func=lambda x: x.group_by("season",num=12*nyears).sel(time=season),
                title=season,
                **kwargs,
                )
            if i > 0:
                ax.set_title("")
    for ax in axes[:-5]:
        ax.set_xticklabels("")
    for i in range(4):
        for ax in axes[4*i+1:4*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
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
    plt.savefig(os.path.join(output_folder,'CO2_tair_anom_lonmean_season'),
                dpi=300,bbox_inches='tight')
    
    # ============== LATMEAN ==================
    fig = plt.figure(figsize=np.multiply((3,3.5),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(4) for j in range(4)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change",fontsize=16)
    kwargs=dict(levels=np.linspace(-3,3,20),
        du=0.5,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        extend='both',
        mean="lat",
        )
    # plots
    axit=iter(axes)
    for i,_ in enumerate(CO2_SOLAR):
        for season in seasons:
            ax=next(axit)
            im=plot_vert(CO2_SOLAR[i],
                ax=ax,
                func=lambda x: x.group_by("season",num=12*nyears).sel(time=season),
                title=season,
                **kwargs,
                )
            if i > 0:
                ax.set_title("")
    for ax in axes[:-5]:
        ax.set_xticklabels("")
    for ax in axes[-5:-1]:
        ax.set_xticklabels(ax.get_xticklabels(),fontsize=7.5)
    for i in range(4):
        for ax in axes[4*i+1:4*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
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
    plt.savefig(os.path.join(output_folder,'CO2_tair_anom_latmean_season'),
                dpi=300,bbox_inches='tight')
tair_anom_season()


# EFFECTIVE RADIATIVE FORCING
def eff_rad():
    grid = GridSpec(3,1,
            left=0.05, right=0.95, top=0.92, bottom=0.15,
            wspace=0.17,hspace=0.40)
    gridcb = GridSpec(1, 1,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((3,3.3),3))
    axes=[fig.add_subplot(grid[i,0],projection=ccrs.PlateCarree()) for i in range(3)] +\
         [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Effective Radiative Forcing",fontsize=16)
    kwargs=dict(levels=np.linspace(-16,16,20),
        du=4,
        cmap=my.Colormaps.div_tsurf,
        add_colorbar=False,
        statistics={'value':'all','fontsize':11,"position":(0.5,-0.15)},
        extend='both',
        )
    # plot
    rad_forcing(CO2_SOLAR[1]).annual_mean().plotvar(
        ax=axes[0],
        title=CO2_SOLAR_titles[1],
        **kwargs,
        )
    rad_forcing(CO2_SOLAR[3]).annual_mean().plotvar(
        ax=axes[1],
        title=CO2_SOLAR_titles[3],
        **kwargs,
        )
    im=rad_forcing(CO2_SOLAR[3],ctrl=CO2_SOLAR[1]).annual_mean().plotvar(
        ax=axes[2],
        title=f"{CO2_SOLAR_titles[3]} - {CO2_SOLAR_titles[1]}",
        **kwargs,
        )
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[W \cdot m^2]$",
        ticks=np.arange(-16,16+4,4),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'Rad_forcing'),
                dpi=300,bbox_inches='tight')
eff_rad()

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
    for i,_ in enumerate(CO2_SOLAR):
        time_series(CO2_SOLAR[i],var=var,moving_average=ma,
            color=CO2_SOLAR_colors[i],label=CO2_SOLAR_titles[i])
    plt.ylabel('[K]')
    plt.xlabel('Year of simulation')
    # plt.ylim(-0.25,1)
    # plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.legend()
    plt.title('Surface Temperature Change')
    plt.savefig(os.path.join(output_folder,'CO2_tsurf_tseries'),
                dpi=300,bbox_inches='tight')
tsurf_tseries()

# PRECIP Time series 
def precip_tseries():
    plt.figure()
    var='precipitation_flux'
    ma=5*12
    func=lambda x: x.to_mm_per_day()
    for i,_ in enumerate(CO2_SOLAR):
        time_series(CO2_SOLAR[i],var=var,moving_average=ma,
            func=func,color=CO2_SOLAR_colors[i],label=CO2_SOLAR_titles[i])
    plt.ylabel('[$mm \cdot d^{-1}]$')
    plt.xlabel('Year of simulation')
    plt.ylim(-0.25,0.25)
    # plt.legend(loc='upper left',bbox_to_anchor=(0.99,1.02))
    plt.legend()
    plt.title('Precipitation Change')
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
        wspace=2.8)
    fig = plt.figure(figsize=np.multiply((5,3),1.7))
    fig.suptitle("Air Temperature",fontsize=16)
    axm = fig.add_subplot(grid[1:3,0:2])
    axz = fig.add_subplot(grid[:,2:])
    # Main Plot
    plot_airprof(data=ctl,other_data=CO2_SOLAR,
            colors=['black']+CO2_SOLAR_colors,
            labels=['Control']+CO2_SOLAR_titles,
            double_axis="height",
            legend=False,
            ax=axm,
            title="")
    axm.set_xlim(150,300)
    # Zoom Plot
    plot_airprof(ax=axz,data=ctl,other_data=CO2_SOLAR,
            colors=['black']+CO2_SOLAR_colors,
            labels=['Control']+CO2_SOLAR_titles,
            double_axis="height",
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
        double_axis="height",
        colors=CO2_SOLAR_colors,
        labels=CO2_SOLAR_titles,
        units='[K]',
        legend=True,
        # legend_kwargs={'loc':'upper left',
        #     'bbox_to_anchor':(1.1,1.02)},
        title='Air Temperature Change')
    plt.savefig(os.path.join(output_folder,'CO2_anom_airprof'),
        dpi=300,bbox_inches='tight')
air_prof_anom()

#====================================================#






