import myfuncs as my
import xarray as xr
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import string
from matplotlib.patches import Rectangle
import matplotlib.colors as colors
import glob
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

mlev = {"la":[1,7],
        "ma":[7,13],
        "ha":[13,19]}
plev = {"la":[1000,870],
        "ma":[870,630],
        "ha":[630,400]}
lat = {"pac":[-20,20],
       "ama":[-20,20],
       "atl":[-20,20],
       "afr":[-20,20],
       "ind":[-20,20],
       "equa":[-10,10],
       "extr":[-90,-35,35,90],
       "glob":[-90,90]}
lon = { "pac":[165,255],
        "ama":[255,345],
        "atl":[288.75,356.25,18.75],
        "afr":[341.25,356.25,71.25],
        "ind":[33.75,123.75],
        "equa":[0,360],
        "extr":[0,360],
        "glob":[0,360]}

nyears=20
input_folder="/g/data/w40/dm5220/data/processed_data"
output_folder="/g/data/w40/dm5220/data/thesis_figures/ch4"
axes_labels=[f"({l})" for l in list(string.ascii_lowercase)]

def sel_lon(x,area):
    if len(lon[area]) == 2:
        return x.sel(longitude=slice(*lon[area])).longitude_mean()
    else:
        cond=np.where(np.logical_or(np.logical_and(x.longitude>=lon[area][0],x.longitude<=lon[area][1]),x.longitude<=lon[area][2]))[0]
        return x.isel(longitude=cond).longitude_mean()

def sel_lat(x,area):
    if len(lat[area]) == 2:
        return x.sel(latitude=slice(*lat[area])).latitude_mean()
    else:
        cond=np.logical_or(np.logical_and(x.latitude>=lat[area][0],x.latitude<=lat[area][1]),
                           np.logical_and(x.latitude>=lat[area][2],x.latitude<=lat[area][3]))
        return x.isel(latitude=cond).latitude_mean()

def rectangle(lat=None,lon=None,lev=None):
    patches=[]
    X=[]
    Y=[]
    
    if lev is None or lat is None:
        if len(lon) > 2:
            lon=[lon[0],lon[2]]
        lon=[l-360 if l >= 180 else l for l in lon]
        if lon[0] < 0:
            lon.sort()
            X.append([lon[0],lon[1]-lon[0]])
        else:
            if lon[1] > 0:
                X.append([lon[0],lon[1]-lon[0]])
            else:
                X.append([lon[0],180-lon[0]])
                X.append([-180,180+lon[1]])
    else:
        X.append([lat[0],lat[1]-lat[0]])
        if len(lat) > 2:
            X.append([lat[2],lat[3]-lat[2]])

    if lev is not None:
        for _ in X:
            Y.append([lev[0],lev[1]-lev[0]])
    else:
        for _ in X:
            Y.append([lat[0],lat[1]-lat[0]])
        if len(lat) > 2:
            Y.append([lat[2],lat[3]-lat[2]])
            Y.append([lat[2],lat[3]-lat[2]])
            X.extend(X)

    for x,y in zip(X,Y):
        patches.append(
            Rectangle((x[0],y[0]),
                       x[1],
                       y[1],
                       fill=False,
                       ls='--',
                       color='red'))
    return patches

def open_(x):
    return xr.open_dataset(os.path.join(input_folder,f"{x}.nc"))

ctl=open_("ctl")
diff_ctl=open_('4co2_fix_tsurf')

filespec=lambda file: file.split('_')  
base_anom=lambda var: diff_ctl[var]-ctl[var]
anom_4co2=lambda data,var: data[var]-diff_ctl[var]
anom_ctl=lambda data,var: data[var]-ctl[var]

area_negative_flux=[
    '4co2_fix_tsurf_m_afr_la',
    '4co2_fix_tsurf_m_afr_ma',
    '4co2_fix_tsurf_m_afr_ha',
    '4co2_fix_tsurf_m_ama_la',
    '4co2_fix_tsurf_m_ama_ma',
    '4co2_fix_tsurf_m_ama_ha',
    '4co2_fix_tsurf_m_atl_la',
    '4co2_fix_tsurf_m_atl_ma',
    '4co2_fix_tsurf_m_atl_ha',
    '4co2_fix_tsurf_m_ind_la',
    '4co2_fix_tsurf_m_ind_ma',
    '4co2_fix_tsurf_m_ind_ha',
    '4co2_fix_tsurf_m_pac_la',
    '4co2_fix_tsurf_m_pac_ma',
    '4co2_fix_tsurf_m_pac_ha',
    ]

area_positive_flux=[
    '4co2_fix_tsurf_p_afr_la',
    '4co2_fix_tsurf_p_afr_ma',
    '4co2_fix_tsurf_p_afr_ha',
    '4co2_fix_tsurf_p_ama_la',
    '4co2_fix_tsurf_p_ama_ma',
    '4co2_fix_tsurf_p_ama_ha',
    '4co2_fix_tsurf_p_atl_la',
    '4co2_fix_tsurf_p_atl_ma',
    '4co2_fix_tsurf_p_atl_ha',
    '4co2_fix_tsurf_p_ind_la',
    '4co2_fix_tsurf_p_ind_ma',
    '4co2_fix_tsurf_p_ind_ha',
    '4co2_fix_tsurf_p_pac_la',
    '4co2_fix_tsurf_p_pac_ma',
    '4co2_fix_tsurf_p_pac_ha',
    ]

area_titles=[
    "Africa LA",
    "Africa MA",
    "Africa HA",
    "Amazon LA",
    "Amazon MA",
    "Amazon HA",
    "Atlantic LA",
    "Atlantic MA",
    "Atlantic HA",
    "Indian LA",
    "Indian MA",
    "Indian HA",
    "Pacific LA",
    "Pacific MA",
    "Pacific HA",
    ]

zonal_negative_flux=[
    '4co2_fix_tsurf_m_equa_la',
    '4co2_fix_tsurf_m_equa_ma',
    '4co2_fix_tsurf_m_extr_la',
    '4co2_fix_tsurf_m_extr_ma',
    '4co2_fix_tsurf_m_glob_la',
    '4co2_fix_tsurf_m_glob_ma',
    ]

zonal_positive_flux=[
    '4co2_fix_tsurf_p_equa_la',
    '4co2_fix_tsurf_p_equa_ma',
    '4co2_fix_tsurf_p_extr_la',
    '4co2_fix_tsurf_p_extr_ma',
    '4co2_fix_tsurf_p_glob_la',
    '4co2_fix_tsurf_p_glob_ma',
    ]

zonal_titles=[
    "Equator LA",
    "Equator MA",
    "Extratropics LA",
    "Extratropics MA",
    "Global LA",
    "Global MA",
    ]

def get_data(file,var="precipitation_flux",control='4co2_fix_tsurf',func=lambda x: x):
    d=open_(file)
    std=func(my.DataArray(base_anom(var))).isel(time=slice(-nyears*12,None)).std('time')
    if control == '4co2_fix_tsurf':
        data=func(my.DataArray(anom_4co2(d,var)))
        P=func(my.DataArray(d[var])).t_student_probability(func(my.DataArray(diff_ctl[var])),num_years=nyears) * data.isel(time=slice(-nyears*12,None)).std('time') / std
    elif control == 'ctl':
        data=func(my.DataArray(anom_ctl(d,var))) 
        P=func(my.DataArray(d[var])).t_student_probability(func(my.DataArray(ctl[var])),num_years=nyears) * data.isel(time=slice(-nyears*12,None)).std('time') / std
    return [data.annual_mean(12*nyears,normalize=std),P]

def plot_anom(file,control='4co2_fix_tsurf',var="precipitation_flux",func=lambda x: x,**kwargs):
    data,P=get_data(file,var,control)
    im=data.plotvar(
        t_student=P,
        **kwargs)
    if ('best' not in file) and (file != "4co2_fix_tsurf"):
        rec=rectangle(lon=lon[filespec(file)[4]],lat=lat[filespec(file)[4]])
        for r in rec:
            if 'ax' in kwargs:
                kwargs['ax'].add_patch(r)
            else:
                plt.gca().add_patch(r)
    return im

def plot_level(file,mean='lonmean',control='4co2_fix_tsurf',var="air_temperature_0_plev",func=lambda x: x*1,**kwargs):
    data,P=get_data(file,var,control)
    if mean == 'lonmean':
        selection=sel_lon
        rec=rectangle(lev=plev[filespec(file)[5]],lat=lat[filespec(file)[4]])
    else:
        selection=sel_lat
        rec=rectangle(lev=plev[filespec(file)[5]],lon=lon[filespec(file)[4]])
    data=selection(data,filespec(file)[4])
    im=data.plotlev(
        t_student=selection(P,filespec(file)[4]),
        **kwargs)
    for r in rec:
        if 'ax' in kwargs:
            kwargs['ax'].add_patch(r)
        else:
            plt.gca().add_patch(r)
    return im

def plot_profile(file,var="air_temperature_0_plev",func=lambda x: x*1,**kwargs):
        d=open_(file)
        data=func(my.DataArray(anom_4co2(d,var)))
        data=sel_lat(sel_lon(data,filespec(file)[4]),filespec(file)[4])
        std=sel_lat(sel_lon(func(my.DataArray(base_anom(var))).isel(time=slice(-nyears*12,None)).std('time'),filespec(file)[4]),filespec(file)[4])
        data=data.annual_mean(12*nyears,normalize=std)
        data.plotprof(
            **kwargs)
        ax=kwargs['ax'] if 'ax' in kwargs else plt.gca()
        xlim=ax.get_xlim()
        ax.hlines(plev[filespec(file)[5]][0],-10,10,color='red',lw=1,ls='--')
        ax.hlines(plev[filespec(file)[5]][1],-10,10,color='red',lw=1,ls='--')
        ax.set_xlim(*xlim)
        ax.set_xlabel("")

# ==================================================================== #
# ==================================================================== #
# ==================================================================== #
        
# Example AFRICA HA
def example_pos_plots():
    ex_pos='4co2_fix_tsurf_p_afr_ha'
    ex_neg='4co2_fix_tsurf_m_afr_ha'
    grid = GridSpec(2,3,
            left=0.27, right=1, top=0.92, bottom=0.32,
            wspace=0.43,hspace=0.20,
            width_ratios=[12.5,12.5,1],height_ratios=[1,0.8])
    grid2 = GridSpec(1,2,
            left=0.25, right=0.95, top=0.25, bottom=0.03,
            wspace=0.2,hspace=0.10, width_ratios=[25,1])
    # === NEGATIVE === #
    fig = plt.figure(figsize=np.multiply((3,3.7),3))
    axes=[fig.add_subplot(grid[0,0]),
          fig.add_subplot(grid[0,1]),
          fig.add_subplot(grid[1,:2]),
          fig.add_subplot(grid2[0,0],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[0,2]),
          fig.add_subplot(grid2[0,1])]
    fig.suptitle("Response of example flux | Negative flux",fontsize=14,x=0.61)
    kwargs=dict(
        levels=np.linspace(-1,1,20),
        du=0.25,
        extend='both',
        add_colorbar=False,
        )
    # tair plots
    im=plot_level(
        ex_neg,
        mean='lonmean',
        ax=axes[0],
        cmap=my.Colormaps.div_tsurf,
        **kwargs
    )
    axes[0].set_title("Air temperature (Lon. mean)",fontsize=9.7)

    plot_level(
        ex_neg,
        mean='latmean',
        ax=axes[1],
        cmap=my.Colormaps.div_tsurf,
        double_axis='height',
        **kwargs
    )
    axes[1].set_yticklabels("")
    axes[1].set_ylabel("")
    axes[1].set_title("Air temperature (Lat. mean)",fontsize=9.7)
    #profile plots
    plot_profile(ex_neg,
            ax=axes[2],
            title="Air temperature profile",
            double_axis='height',
            )
    axes[2].set_xlabel('$[K]$')
    axes[2].set_xlim(-1.5,1.5)
    axes[2].set_xticks(np.arange(-1.5,1.5+.5,.5))
    axes[2].set_xticklabels([str(t) for t in np.arange(-1.5,1.5+.5,.5)])
    # precip plots
    im2=plot_anom(
        ex_neg,
        ax=axes[3],
        title="Precipitation",
        cmap=my.Colormaps.div_precip,
        double_axis='height',
        func=lambda x: x.to_mm_per_day(),
        **kwargs
        )
    # plot colorbars
    plt.colorbar(im,cax=axes[-2],
        orientation="vertical",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    plt.colorbar(im2,cax=axes[-1],
        orientation="vertical",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    label=iter(axes_labels)
    for ax in axes[:-2]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'example_negative'),
            dpi=300,bbox_inches='tight')
    
    # === POSITIVE === #
    fig = plt.figure(figsize=np.multiply((3,3.7),3))
    axes=[fig.add_subplot(grid[0,0]),
          fig.add_subplot(grid[0,1]),
          fig.add_subplot(grid[1,:2]),
          fig.add_subplot(grid2[0,0],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid[0,2]),
          fig.add_subplot(grid2[0,1])]
    fig.suptitle("Response of example flux | Positive flux",fontsize=14,x=0.61)
    kwargs=dict(
        levels=np.linspace(-1,1,20),
        du=0.25,
        extend='both',
        add_colorbar=False,
        )
    # tair plots
    im=plot_level(
        ex_pos,
        mean='lonmean',
        ax=axes[0],
        cmap=my.Colormaps.div_tsurf,
        **kwargs
    )
    axes[0].set_title("Air temperature (Lon. mean)",fontsize=9.7)

    plot_level(
        ex_pos,
        mean='latmean',
        ax=axes[1],
        cmap=my.Colormaps.div_tsurf,
        double_axis='height',
        **kwargs
    )
    axes[1].set_yticklabels("")
    axes[1].set_ylabel("")
    axes[1].set_title("Air temperature (Lat. mean)",fontsize=9.7)
    #profile plots
    plot_profile(ex_pos,
            ax=axes[2],
            title="Air temperature profile",
            double_axis='height',
            )
    axes[2].set_xlabel('$[K]$')
    axes[2].set_xlim(-1.5,1.5)
    axes[2].set_xticks(np.arange(-1.5,1.5+.5,.5))
    axes[2].set_xticklabels([str(t) for t in np.arange(-1.5,1.5+.5,.5)])
    # precip plots
    im2=plot_anom(
        ex_pos,
        ax=axes[3],
        title="Precipitation",
        cmap=my.Colormaps.div_precip,
        double_axis='height',
        func=lambda x: x.to_mm_per_day(),
        **kwargs
        )
    # plot colorbars
    plt.colorbar(im,cax=axes[-2],
        orientation="vertical",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    plt.colorbar(im2,cax=axes[-1],
        orientation="vertical",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    label=iter(axes_labels)
    for ax in axes[:-2]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'example_positive'),
            dpi=300,bbox_inches='tight')
example_pos_plots()
    
# Example flux
def example_flux_pos():
    ex_flux=my.open_dataarray("/g/data/w40/dm5220/ancil/user_mlevel/tac_rad_change/files_for_xancil/p_afr_ha.nc")
    grid = GridSpec(1,1,
            left=0.1, right=0.9, top=0.92, bottom=0.69,
            wspace=0.2,hspace=0.10)
    grid2 = GridSpec(2,1,
            left=0.2, right=0.8, top=0.64, bottom=0.04,
            wspace=0.33,hspace=0.20)
    # === POSITIVE === #
    fig = plt.figure(figsize=np.multiply((3,3.7),3))
    axes=[fig.add_subplot(grid[0,0],projection=ccrs.PlateCarree()),
          fig.add_subplot(grid2[0,0]),
          fig.add_subplot(grid2[1,0]),
          ]
    fig.suptitle("Example of atmospheric flux",fontsize=14)
    data=ex_flux.annual_mean()
    # lat-lon
    data.sel(model_level_number=13).plotvar(
        ax=axes[0],
        cmap=mpl.colors.ListedColormap(['white', 'red']),
        add_colorbar=False,
        statistics=False,
        title="Map")
    # lev 
    data.longitude_mean().plotlev(
        ax=axes[1],
        cmap=mpl.colors.ListedColormap(['white', 'red']),
        add_colorbar=False,
        double_axis='pressure',
        title="Latitudinal profile")
    data.latitude_mean().plotlev(
        ax=axes[2],
        cmap=mpl.colors.ListedColormap(['white', 'red']),
        add_colorbar=False,
        double_axis='pressure',
        title="Longitudinal profile")
    rec=Rectangle(
        (0.85,1.05),
        0.06,
        0.1,
        fill=True,
        color='red',
        transform=axes[0].transAxes,
        clip_on=False)
    axes[0].add_patch(rec)
    axes[0].text(
        0.92,1.1,
        "= 0.02 $K/(30min)$",
        fontsize=10,
        ha='left',
        va='center',
        transform=axes[0].transAxes)
    label=iter(axes_labels)
    for ax in axes:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'example_flux'),
            dpi=300,bbox_inches='tight')
example_flux_pos()

#=== AREA EXP ===#
def precip_anom_area():
    grid = GridSpec(5,3,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 3,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ====== NEGATIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((3,3.5),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(5) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation change | Negative flux",fontsize=14)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        grid=False
        )
    # plots
    for i,_ in enumerate(area_negative_flux):
        ypos=-0.06 if i<12 else -0.17
        im=plot_anom(area_negative_flux[i],
            ax=axes[i],
            title=area_titles[i],
            statistics={'value':'all','fontsize':8,"position":(0.5,ypos)},
            **kwargs,
            )
    for ax in [axes[i] for i in [1,2,4,5,7,8,10,11]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    for ax in [axes[i] for i in [0,3,6,9]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
        gl.left_labels=True
    for ax in [axes[i] for i in [13,14]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
        gl.bottom_labels=True
    gl=axes[12].gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    gl.bottom_labels=True
    gl.left_labels=True
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_negative_precip'),
                dpi=300,bbox_inches='tight')
    
    # ====== POSITIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((3,3.5),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(5) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation change | Positive flux",fontsize=14)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        grid=False
        )
    # plots
    for i,_ in enumerate(area_positive_flux):
        ypos=-0.06 if i<12 else -0.17
        im=plot_anom(area_positive_flux[i],
            ax=axes[i],
            title=area_titles[i],
            statistics={'value':'all','fontsize':8,"position":(0.5,ypos)},
            **kwargs,
            )
    for ax in [axes[i] for i in [1,2,4,5,7,8,10,11]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    for ax in [axes[i] for i in [0,3,6,9]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
        gl.left_labels=True
    for ax in [axes[i] for i in [13,14]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
        gl.bottom_labels=True
    gl=axes[12].gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    gl.bottom_labels=True
    gl.left_labels=True
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_positive_precip'),
                dpi=300,bbox_inches='tight')
precip_anom_area()

def tair_anom_area():
    grid = GridSpec(5,3,
            left=0.08, right=0.92, top=0.91, bottom=0.13,
            wspace=0.4,hspace=0.3)
    gridcb = GridSpec(1, 3,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    # ====== NEGATIVE FLUX ====== #
    # ====== LONMEAN ====== #
    axes=[fig.add_subplot(grid[i,j]) for i in range(5) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air temperature change | Negative flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(area_negative_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        im=plot_level(area_negative_flux[i],
            mean='lonmean',
            ax=axes[i],
            title=area_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-4]:
        ax.set_xticklabels("")
    for i in range(5):
        for ax in axes[3*i+1:3*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_negative_tair_lonmean'),
                dpi=300,bbox_inches='tight')
    
    # ====== LATMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(5) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air temperature change | Negative flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(area_negative_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        im=plot_level(area_negative_flux[i],
            mean='latmean',
            ax=axes[i],
            title=area_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-4]:
        ax.set_xticklabels("")
    for ax in axes[-4:-1]:
        ax.set_xticklabels(ax.get_xticklabels(),fontsize=7.5)
    for i in range(5):
        for ax in axes[3*i+1:3*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_negative_tair_latmean'),
                dpi=300,bbox_inches='tight')
    
    # ====== POSITIVE FLUX ====== #
    # ====== LONMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(5) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air temperature change | Positive flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(area_positive_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        im=plot_level(area_positive_flux[i],
            mean='lonmean',
            ax=axes[i],
            title=area_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-4]:
        ax.set_xticklabels("")
    for i in range(5):
        for ax in axes[3*i+1:3*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_positive_tair_lonmean'),
                dpi=300,bbox_inches='tight')
    
    # ====== LATMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(5) for j in range(3)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air temperature change | Positive flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(area_positive_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        im=plot_level(area_positive_flux[i],
            mean='latmean',
            ax=axes[i],
            title=area_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-4]:
        ax.set_xticklabels("")
    for ax in axes[-4:-1]:
        ax.set_xticklabels(ax.get_xticklabels(),fontsize=7.5)
    for i in range(5):
        for ax in axes[3*i+1:3*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_positive_tair_latmean'),
                dpi=300,bbox_inches='tight')
tair_anom_area()

def tair_prof_area():
    grid = GridSpec(5,3,
            left=0.08, right=0.92, top=0.91, bottom=0.05,
            wspace=0.4,hspace=0.3)
    # ====== NEGATIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.6),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(5) for j in range(3)]
    fig.suptitle("Air temperature profiles | Negative flux",fontsize=14)
    kwargs=dict(
        )
    # plots
    for i,_ in enumerate(area_negative_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        plot_profile(area_negative_flux[i],
            ax=axes[i],
            title=area_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes:
        ax.set_xlim(-1.5,1.5)
        ax.set_xticks(np.arange(-1.5,1.5+.5,.5))
        ax.set_xticklabels([str(t) for t in np.arange(-1.5,1.5+.5,.5)],fontsize=9)
    for ax in axes[:-3]:
        ax.set_xticklabels("")
    for ax in axes[-3:]:
        ax.set_xlabel("$[K]$")
    for i in range(5):
        for ax in axes[3*i+1:3*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
    # Label subplots
    label=iter(axes_labels)
    for ax in axes:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_negative_tair_profiles'),
                dpi=300,bbox_inches='tight')
    
    # ====== POSITIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.6),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(5) for j in range(3)]
    fig.suptitle("Air temperature profiles | Positive flux",fontsize=14)
    kwargs=dict(
        )
    # plots
    for i,_ in enumerate(area_positive_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        plot_profile(area_positive_flux[i],
            ax=axes[i],
            title=area_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes:
        ax.set_xlim(-1.5,1.5)
        ax.set_xticks(np.arange(-1.5,1.5+.5,.5))
        ax.set_xticklabels([str(t) for t in np.arange(-1.5,1.5+.5,.5)],fontsize=9)
    for ax in axes[:-3]:
        ax.set_xticklabels("")
    for ax in axes[-3:]:
        ax.set_xlabel("$[K]$")
    for i in range(5):
        for ax in axes[3*i+1:3*(i+1)]:
            ax.set_yticklabels("")
            ax.set_ylabel("")
    # Label subplots
    label=iter(axes_labels)
    for ax in axes:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_box_positive_tair_profiles'),
                dpi=300,bbox_inches='tight')
tair_prof_area()

#=== ZONAL EXP ===#
def precip_anom_zonal():
    grid = GridSpec(3,2,
            left=0.05, right=0.95, top=0.95, bottom=0.12,
            wspace=0.17,hspace=0.10)
    gridcb = GridSpec(1, 2,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ====== NEGATIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((2.8,3.2),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation Change | Negative flux",fontsize=14)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        grid=False
        )
    # plots
    for i,_ in enumerate(zonal_negative_flux):
        ypos=-0.06 if i<4 else -0.17
        im=plot_anom(zonal_negative_flux[i],
            ax=axes[i],
            title=zonal_titles[i],
            statistics={'value':'all','fontsize':8,"position":(0.5,ypos)},
            **kwargs,
            )
    for ax in [axes[i] for i in [1,3]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    for ax in [axes[i] for i in [0,2]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
        gl.left_labels=True
    gl=axes[4].gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    gl.bottom_labels=True
    gl.left_labels=True
    gl=axes[5].gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    gl.bottom_labels=True
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_negative_precip'),
                dpi=300,bbox_inches='tight')
    
    # ====== POSITIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((2.8,3.2),3))
    axes=[fig.add_subplot(grid[i,j],projection=ccrs.PlateCarree()) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Precipitation Change | Positive flux",fontsize=14)
    kwargs=dict(func=lambda x: x.to_mm_per_day(),
        var="precipitation_flux",
        levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_precip,
        add_colorbar=False,
        extend='both',
        grid=False
        )
    # plots
    for i,_ in enumerate(zonal_positive_flux):
        ypos=-0.06 if i<4 else -0.17
        im=plot_anom(zonal_positive_flux[i],
            ax=axes[i],
            title=zonal_titles[i],
            statistics={'value':'all','fontsize':8,"position":(0.5,ypos)},
            **kwargs,
            )
    for ax in [axes[i] for i in [1,3]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    for ax in [axes[i] for i in [0,2]]:
        gl=ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
        gl.left_labels=True
    gl=axes[4].gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    gl.bottom_labels=True
    gl.left_labels=True
    gl=axes[5].gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='grey', alpha=0.3, linestyle='--')
    gl.bottom_labels=True
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_positive_precip'),
                dpi=300,bbox_inches='tight')
precip_anom_zonal()

def tair_anom_zonal():
    grid = GridSpec(3,2,
            left=0.08, right=0.92, top=0.91, bottom=0.13,
            wspace=0.3,hspace=0.3)
    gridcb = GridSpec(1, 3,
            left=0.05, right=0.95, top=0.08, bottom=0.05)
    # ====== NEGATIVE FLUX ====== #
    # ====== LONMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change | Negative flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(zonal_negative_flux):
        dax = 'height' if np.mod(i,2) == 1 else False
        im=plot_level(zonal_negative_flux[i],
            mean='lonmean',
            ax=axes[i],
            title=zonal_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-3]:
        ax.set_xticklabels("")
    for ax in [axes[i] for i in [1,3,5]]:
        ax.set_yticklabels("")
        ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_negative_tair_lonmean'),
                dpi=300,bbox_inches='tight')
    
    # ====== LATMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change | Negative flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(zonal_negative_flux):
        dax = 'height' if np.mod(i,2) == 1 else False
        im=plot_level(zonal_negative_flux[i],
            mean='latmean',
            ax=axes[i],
            title=zonal_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-3]:
        ax.set_xticklabels("")
    for ax in [axes[i] for i in [1,3,5]]:
        ax.set_yticklabels("")
        ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_negative_tair_latmean'),
                dpi=300,bbox_inches='tight')
    
    # ====== POSITIVE FLUX ====== #
    # ====== LONMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change | Positive flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(zonal_positive_flux):
        dax = 'height' if np.mod(i,2) == 1 else False
        im=plot_level(zonal_positive_flux[i],
            mean='lonmean',
            ax=axes[i],
            title=zonal_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-3]:
        ax.set_xticklabels("")
    for ax in [axes[i] for i in [1,3,5]]:
        ax.set_yticklabels("")
        ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_positive_tair_lonmean'),
                dpi=300,bbox_inches='tight')
    
    # ====== LATMEAN ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.8),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)] + [fig.add_subplot(gridcb[:,:])]
    fig.suptitle("Air Temperature Change | Positive flux",fontsize=14)
    kwargs=dict(levels=np.linspace(-1,1,20),
        du=0.25,
        cmap=my.Colormaps.div_tsurf,
        extend='both',
        add_colorbar=False,
        )
    # plots
    for i,_ in enumerate(zonal_positive_flux):
        dax = 'height' if np.mod(i,2) == 1 else False
        im=plot_level(zonal_positive_flux[i],
            mean='latmean',
            ax=axes[i],
            title=zonal_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes[:-3]:
        ax.set_xticklabels("")
    for ax in [axes[i] for i in [1,3,5]]:
        ax.set_yticklabels("")
        ax.set_ylabel("")
    # plot colorbar   
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[K]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    # Label subplots
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_positive_tair_latmean'),
                dpi=300,bbox_inches='tight')
tair_anom_zonal()

def tair_prof_zonal():
    grid = GridSpec(3,2,
            left=0.08, right=0.92, top=0.91, bottom=0.05,
            wspace=0.3,hspace=0.3)
    # ====== NEGATIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.6),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)]
    fig.suptitle("Air temperature profiles | Negative flux",fontsize=14)
    kwargs=dict(
        )
    # plots
    for i,_ in enumerate(zonal_negative_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        plot_profile(zonal_negative_flux[i],
            ax=axes[i],
            title=zonal_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes:
        ax.set_xlim(-1.5,1.5)
        ax.set_xticks(np.arange(-1.5,1.5+.5,.5))
        ax.set_xticklabels([str(t) for t in np.arange(-1.5,1.5+.5,.5)],fontsize=9)
    for ax in axes[:-2]:
        ax.set_xticklabels("")
    for ax in axes[-2:]:
        ax.set_xlabel("$[K]$")
    for ax in [axes[i] for i in [1,3,5]]:
        ax.set_yticklabels("")
        ax.set_ylabel("")
    # Label subplots
    label=iter(axes_labels)
    for ax in axes:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_negative_tair_profiles'),
                dpi=300,bbox_inches='tight')
    
    # ====== POSITIVE FLUX ====== #
    fig = plt.figure(figsize=np.multiply((2.7,3.6),3))
    axes=[fig.add_subplot(grid[i,j]) for i in range(3) for j in range(2)]
    fig.suptitle("Air temperature profiles | Positive flux",fontsize=14)
    kwargs=dict(
        )
    # plots
    for i,_ in enumerate(zonal_positive_flux):
        dax = 'height' if np.mod(i+1,3) == 0 else False
        plot_profile(zonal_positive_flux[i],
            ax=axes[i],
            title=zonal_titles[i],
            double_axis=dax,
            **kwargs,
            )
    for ax in axes:
        ax.set_xlim(-1.5,1.5)
        ax.set_xticks(np.arange(-1.5,1.5+.5,.5))
        ax.set_xticklabels([str(t) for t in np.arange(-1.5,1.5+.5,.5)],fontsize=9)
    for ax in axes[:-2]:
        ax.set_xticklabels("")
    for ax in axes[-2:]:
        ax.set_xlabel("$[K]$")
    for ax in [axes[i] for i in [1,3,5]]:
        ax.set_yticklabels("")
        ax.set_ylabel("")
    # Label subplots
    label=iter(axes_labels)
    for ax in axes:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'sensexp_zonal_positive_tair_profiles'),
                dpi=300,bbox_inches='tight')
tair_prof_zonal()

# =============================== #
#=== COMPARE JOINT EXPERIMENTS ===#
def compare():
    files=glob.glob(os.path.join(input_folder,"4co2_fix_tsurf_best*"))
    files=[f.split("processed_data/")[1][:-3] for f in files]
    indeces=[int(f.split('best')[1]) for f in files]
    indeces,files=[a[0] for a in sorted(zip(indeces,files))],[a[1] for a in sorted(zip(indeces,files))]
    var="precipitation_flux"

    gm=[]
    gm_tr=[]
    gm_nh=[]
    gm_sh=[]
    rms=[]
    rms_tr=[]
    rms_nh=[]
    rms_sh=[]

    # NO FLUX
    std=my.DataArray(base_anom(var)).to_mm_per_day().isel(time=slice(-nyears*12,None)).std('time')
    d=my.DataArray(base_anom(var)).to_mm_per_day().annual_mean(nyears*20,normalize=std)
    tr=d.sel(latitude=slice(-30,30))
    nh=d.sel(latitude=slice(30,90))
    sh=d.sel(latitude=slice(-90,-30))
    gm.append(d.global_mean().values)
    rms.append(d.rms().values)
    gm_tr.append(tr.global_mean().values)
    rms_tr.append(tr.rms().values)
    gm_nh.append(nh.global_mean().values)
    rms_nh.append(nh.rms().values)
    gm_sh.append(sh.global_mean().values)
    rms_sh.append(sh.rms().values)

    for f in files:
        d=my.DataArray(anom_ctl(open_(f),var)).to_mm_per_day().annual_mean(nyears*20,normalize=std)
        gm.append(d.global_mean().values)
        rms.append(d.rms().values)
        tr=d.sel(latitude=slice(-30,30))
        nh=d.sel(latitude=slice(30,90))
        sh=d.sel(latitude=slice(-90,-30))
        gm_tr.append(tr.global_mean().values)
        rms_tr.append(tr.rms().values)
        gm_nh.append(nh.global_mean().values)
        rms_nh.append(nh.rms().values)
        gm_sh.append(sh.global_mean().values)
        rms_sh.append(sh.rms().values)
    
    def plot_compare():
        # PLOTS
        grid = GridSpec(2,2,
                left=0.01, right=0.98, top=0.92, bottom=0.01,
                wspace=0.5,hspace=0.23)
        fig = plt.figure(figsize=np.multiply((3,3.2),3))
        axes=[fig.add_subplot(grid[0,0]),
            fig.add_subplot(grid[0,1]),
            fig.add_subplot(grid[1,0]),
            fig.add_subplot(grid[1,1])]
        fig.suptitle("Performance of the mitigation experiments",fontsize=15)
        kwargs=dict(
            levels=np.linspace(-1,1,20),
            du=0.25,
            extend='both',
            add_colorbar=False,
            )
        # PLOT GLOBAL
        color1='blue'
        color2='green'
        ax1=axes[0]
        ax1.plot(gm,marker='o',color=color1,markersize=3)
        ax1.set_xticks(np.arange(len(gm)))
        ax1.set_xticklabels(['NO FLUX']+["" if n%2==0 else [f'Exp. {i}' for i in indeces][n] for n,i in enumerate([f'Exp. {i}' for i in indeces])], fontsize=8, rotation=85)
        ax1.set_ylabel('Global Mean Precipitation $[mm \cdot d^{-1}]$',color=color1)
        ax1.grid()
        ax2 = ax1.twinx()
        color='green'
        ax2.plot(rms,marker='o',color=color2,markersize=3)
        ax2.set_ylabel('RMS',color=color2)
        ax1.set_title('Global')

        # PLOT NORTHERN HEMISPHERE
        ax1=axes[1]
        ax1.plot(gm_nh,marker='o',color=color1,markersize=3)
        ax1.set_xticks(np.arange(len(gm_nh)))
        ax1.set_xticklabels(['NO FLUX']+["" if n%2==0 else [f'Exp. {i}' for i in indeces][n] for n,i in enumerate([f'Exp. {i}' for i in indeces])], fontsize=8, rotation=85)
        ax1.set_ylabel('Global Mean Precipitation $[mm \cdot d^{-1}]$',color=color1)
        ax1.grid()
        ax2 = ax1.twinx()
        color='green'
        ax2.plot(rms_nh,marker='o',color=color2,markersize=3)
        ax2.set_ylabel('RMS',color=color2)
        ax1.set_title('Northern Hemisphere (30°N÷90°N)')

        # PLOT TROPICS
        ax1=axes[2]
        ax1.plot(gm_tr,marker='o',color=color1,markersize=3)
        ax1.set_xticks(np.arange(len(gm_tr)))
        ax1.set_xticklabels(['NO FLUX']+["" if n%2==0 else [f'Exp. {i}' for i in indeces][n] for n,i in enumerate([f'Exp. {i}' for i in indeces])], fontsize=8, rotation=85)
        ax1.set_ylabel('Global Mean Precipitation $[mm \cdot d^{-1}]$',color=color1)
        ax1.grid()
        ax2 = ax1.twinx()
        color='green'
        ax2.plot(rms_tr,marker='o',color=color2,markersize=3)
        ax2.set_ylabel('RMS',color=color2)
        ax1.set_title('Tropics (30°S÷30°N)')

        # PLOT SOUTHERN HEMISPHERE
        ax1=axes[3]
        ax1.plot(gm_sh,marker='o',color=color1,markersize=3)
        ax1.set_xticks(np.arange(len(gm_sh)))
        ax1.set_xticklabels(['NO FLUX']+["" if n%2==0 else [f'Exp. {i}' for i in indeces][n] for n,i in enumerate([f'Exp. {i}' for i in indeces])], fontsize=8, rotation=85)
        ax1.set_ylabel('Global Mean Precipitation $[mm \cdot d^{-1}]$',color=color1)
        ax1.grid()
        ax2 = ax1.twinx()
        color='green'
        ax2.plot(rms_sh,marker='o',color=color2,markersize=3)
        ax2.set_ylabel('RMS',color=color2)
        ax1.set_title('Southern Hemisphere (90°S÷30°S)')
        label=iter(axes_labels)
        for ax in axes:
            ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
        plt.savefig(os.path.join(output_folder,'performance_mitigation_exp'),
                    dpi=300,bbox_inches='tight')
    plot_compare()
compare()

# === PLOT EXAMPLE OF FLUX FOR EXPERIMENT 35 === #
def exp35_flux():
    lat,lon,lev=0,0,9
        # PLOT LON
    def plon(x,**kwargs):
        s=x.sel(latitude=lat,model_level_number=lev)[0]
        s.plot(color='blue',**kwargs)
        ax = kwargs['ax'] if 'ax' in kwargs else plt.gca()
        ax.set_xlim([0,360])
        ax.set_ylim([-0.015,0.015])
        ax.set_ylabel("K/(30min)")
        ax.set_xlabel("Longitude")
        ax.xaxis.set_major_locator(MultipleLocator(60))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        ax.set_title(f'Longitudinal profile')
        ax.grid(visible=True,which='both')
        
    # PLOT LAT
    def plat(x,**kwargs):
        ax = kwargs['ax'] if 'ax' in kwargs else plt.gca()
        s=x.sel(longitude=lon,model_level_number=lev)[0]
        s.plot(color='green',**kwargs)
        ax.set_xlim([-90,90])
        ax.set_ylim([-0.015,0.015])
        ax.set_ylabel("K/(30min)")
        ax.set_xlabel("Latitude")
        ax.xaxis.set_major_locator(MultipleLocator(30))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        ax.set_title(f'Latitudinal profile')
        ax.grid(visible=True,which='both')

    # PLOT LEV
    def plev(x,**kwargs):
        ax = kwargs['ax'] if 'ax' in kwargs else plt.gca()
        x=x.sel(model_level_number=slice(0,21))
        s=x.sel(latitude=lat,longitude=lon)[0]
        s.plot(y='model_level_number',color='red',**kwargs)
        ax.set_ylim([1,21])
        ax.set_xlim([-0.015,0.015])
        ax.set_ylabel("Model level number")
        ax.set_xlabel("K/(30min)")
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        ax.set_title(f'Verical profile')
        ax.grid(visible=True,which='both')

    # # PLOT 3D
    def pp(data,**kwargs):
        ax = kwargs.pop('ax') if 'ax' in kwargs else plt.axes(projection="3d")
        x = data.latitude
        y = data.longitude
        z = data.model_level_number.sel(model_level_number=slice(1,22))
        A,B,C = np.meshgrid(x, y, z)
        # Your 4dimension, only for example use yours
        K = np.transpose(data.isel(time=0).sel(model_level_number=slice(1,22)).values,(2,1,0))
        K = np.where(K==0,np.nan,K)
        # cmap=my.Colormaps.div_precip.copy().set_bad([0,0,0,0])
        alpha=0.1
        alpha2=0.6
        colorArray=[[0,0,1,alpha],[0,1,1,alpha],[0,1,0,alpha],[1,1,0,alpha],[1,0,0,alpha]]
        colorArray2=[[0,0,1,alpha2],[0,1,1,alpha2],[0,1,0,alpha2],[1,1,0,alpha2],[1,0,0,alpha2]]
        cmap=colors.LinearSegmentedColormap.from_list('mycmap',colors=colorArray,N=256)
        cmap.set_bad([0,0,0,0])
        cmap2=colors.LinearSegmentedColormap.from_list('mycmap2',colors=colorArray2,N=256)
        cmap2=my.Colormaps.add_white_inbetween(cmap2)
        cmap2.set_bad([0,0,0,0])
        # Creating plot
        ax.view_init(elev=35, azim=70)
        ax.scatter3D(A,B,C, c=K, marker='.',cmap=cmap,
            norm=colors.TwoSlopeNorm(vmin=-0.02,vmax=0.02,vcenter=0),**kwargs)
        img=ax.scatter3D(A,B,C, c=K, marker='.',cmap=cmap2,
            norm=colors.TwoSlopeNorm(vmin=-0.02,vmax=0.02,vcenter=0),**kwargs,visible=False)
        plt.colorbar(img,
            ax=ax,
            label="$K/(30min)$",
            ticks=np.arange(-0.02,0.02+0.005,0.005),
            )
        ax.set_title(f'3D view')
        # xaxis
        ax.set_xlabel("Latitude")
        ax.set_xlim(-90,90)
        ax.xaxis.set_major_locator(MultipleLocator(30))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        # yaxis
        ax.set_ylabel("Longitude")
        ax.set_ylim(0,360)
        ax.yaxis.set_major_locator(MultipleLocator(60))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.yaxis.set_minor_locator(MultipleLocator(30))
        # zaxis
        ax.set_zlabel("Model Level Number")
        ax.set_zlim(0,21)
        ax.zaxis.set_major_locator(MultipleLocator(7))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.zaxis.set_minor_locator(MultipleLocator(1))
        # Plot lev line 
        x1 = (lat,lat)
        y1 = (lon,lon)
        z1 = ax.get_zlim()
        ax.plot(x1,y1,z1,ls='--',alpha=0.8, lw=1,color='red')
        # Plot lon line 
        x1 = (lat,lat)
        y1 = ax.get_ylim()
        z1 = (lev,lev)
        ax.plot(x1,y1,z1,ls='--',alpha=0.8, lw=1,color='blue')
        # Plot lat line 
        x1 = ax.get_xlim()
        y1 = (lon,lon)
        z1 = (lev,lev)
        ax.plot(x1,y1,z1,ls='--',alpha=0.8, lw=1,color='green')
            
    flux=my.open_dataarray("/g/data/w40/dm5220/ancil/user_mlevel/tac_rad_change/files_for_xancil/best35.nc")._to_contiguous_lon()
    grid = GridSpec(2,2,
            left=0.01, right=0.99, top=0.92, bottom=0.01,
            wspace=0.3,hspace=0.3)
    fig = plt.figure(figsize=np.multiply((3,3.2),3))
    axes=[fig.add_subplot(grid[0,0]),
          fig.add_subplot(grid[0,1]),
          fig.add_subplot(grid[1,0]),
          fig.add_subplot(grid[1,1],projection="3d")]
    fig.suptitle("Exp. 35 atmospheric flux",fontsize=15)
    # PLOTS
    plon(flux,ax=axes[0])
    plat(flux,ax=axes[1])
    plev(flux,ax=axes[2])
    pp(flux,ax=axes[3])
    label=iter(axes_labels)
    for ax in axes:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'exp35_flux'),
            dpi=300,bbox_inches='tight')
exp35_flux()

# === EXAMPLE OF BEST EXPERIMENT === #
def best():
    # Get global means and rms
    d1=get_data("4co2_fix_tsurf",control='ctl')[0]
    d2=get_data("4co2_fix_tsurf_best35",control='ctl')[0]
    gmsh1=d1.sel(latitude=slice(-90,-30)).global_mean().values
    gmsh2=d2.sel(latitude=slice(-90,-30)).global_mean().values
    gmnh1=d1.sel(latitude=slice(30,90)).global_mean().values
    gmnh2=d2.sel(latitude=slice(30,90)).global_mean().values
    gmtr1=d1.sel(latitude=slice(-30,30)).global_mean().values
    gmtr2=d2.sel(latitude=slice(-30,30)).global_mean().values
    rmssh1=d1.sel(latitude=slice(-90,-30)).rms().values
    rmssh2=d2.sel(latitude=slice(-90,-30)).rms().values
    rmsnh1=d1.sel(latitude=slice(30,90)).rms().values
    rmsnh2=d2.sel(latitude=slice(30,90)).rms().values
    rmstr1=d1.sel(latitude=slice(-30,30)).rms().values
    rmstr2=d2.sel(latitude=slice(-30,30)).rms().values
    grid = GridSpec(3,1,
            left=0.01, right=0.98, top=0.92, bottom=0.01,
            wspace=0.5,hspace=0.55, height_ratios=[12.5,12.5,1])
    fig = plt.figure(figsize=np.multiply((3,3.4),3))
    axes=[fig.add_subplot(grid[0,0],projection=ccrs.PlateCarree()),
        fig.add_subplot(grid[1,0],projection=ccrs.PlateCarree()),
        fig.add_subplot(grid[2,0])]
    fig.suptitle("Precipitation change",fontsize=14)
    kwargs=dict(
        levels=np.linspace(-1,1,20),
        du=0.25,
        extend='both',
        add_colorbar=False,
        control='ctl',
        )
    # PLOT 4co2_fix_tsurf
    im=plot_anom("4co2_fix_tsurf",
        ax=axes[0],
        title="4CO2 FIX TSURF",
        **kwargs)
    axes[0].text(0.15,-0.25,
        f"Southern Hemisphere\ngmean = {gmsh1:.2f} | rms = {rmssh1:.2f}",
        fontsize=9,
        color='blue',
        ha='center',
        fontweight='bold',
        transform=axes[0].transAxes,
        )
    axes[0].text(0.5,-0.25,
        f"Tropics\ngmean = {gmtr1:.2f} | rms = {rmstr1:.2f}",
        fontsize=9,
        color='red',
        ha='center',
        fontweight='bold',
        transform=axes[0].transAxes,
        )
    axes[0].text(0.85,-0.25,
        f"Northern Hemisphere\ngmean = {gmnh1:.2f} | rms = {rmsnh1:.2f}",
        fontsize=9,
        color='green',
        ha='center',
        fontweight='bold',
        transform=axes[0].transAxes,
        )
    # PLOT 4co2_fix_tsurf_best31 
    plot_anom("4co2_fix_tsurf_best31",
        ax=axes[1],
        title="MITIGATION EXP. 35",
        **kwargs)
    axes[1].text(0.15,-0.25,
        f"Southern Hemisphere\ngmean = {gmsh2:.2f} | rms = {rmssh2:.2f}",
        fontsize=9,
        color='blue',
        ha='center',
        fontweight='bold',
        transform=axes[1].transAxes,
        )
    axes[1].text(0.5,-0.25,
        f"Tropics\ngmean = {gmtr2:.2f} | rms = {rmstr2:.2f}",
        fontsize=9,
        color='red',
        ha='center',
        fontweight='bold',
        transform=axes[1].transAxes,
        )
    axes[1].text(0.85,-0.25,
        f"Northern Hemisphere\ngmean = {gmnh2:.2f} | rms = {rmsnh2:.2f}",
        fontsize=9,
        color='green',
        ha='center',
        fontweight='bold',
        transform=axes[1].transAxes,
        )
    # Plot colorbar
    plt.colorbar(im,cax=axes[-1],
        orientation="horizontal",
        label="$[mm \cdot d^{-1}]$",
        ticks=np.arange(-1,1+0.25,0.25),
        )
    label=iter(axes_labels)
    for ax in axes[:-1]:
        ax.set_title(next(label), fontfamily='serif', loc='left', fontsize='large')
    plt.savefig(os.path.join(output_folder,'best_exp_precip'),
                dpi=300,bbox_inches='tight')
best()
