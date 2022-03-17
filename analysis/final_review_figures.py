import myfuncs as my
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature

nyears = 20
# REPORT
ctl=my.UM.read_data('ctl')

anomalies = lambda x,var: x[var] - ctl[var]
P = lambda x,var: x[var].t_student_probability(ctl[var])

co2x4=my.UM.read_data('4co2')
solar50p=my.UM.read_data('ctl_solar50+')
co2x4_fix=my.UM.read_data('4co2_fix_tsurf')
solar50p_fix=my.UM.read_data('ctl_fix_tsurf_solar50+')
co2x4_SWm=my.UM.read_data('4co2_sw_x0.9452_offset')
solar50p_SWm=my.UM.read_data('ctl_solar50+_sw-_x0.9489_offset')

all_data=[
    co2x4,
    solar50p,
    co2x4_fix,
    co2x4_SWm,
    solar50p_fix,
    solar50p_SWm,
] 
titles=[
    '4CO2',
    'Solar50+',
    '4CO2 SW-',
    '4CO2 fix',
    'Solar50+ fix',
    'Solar50+ SW-',
] 

output_folder="/g/data/w40/dm5220/data/final_review_figures"
os.makedirs(output_folder,exist_ok=True)

# FIGURES FOR REPORT
def plot_tsurf():
    plt.rcParams.update({'font.size': 11})
    var='surface_temperature'
    gs = GridSpec(3, 3, height_ratios=[8,8,1],
                wspace=0.15,hspace=0)
    fig=plt.figure(figsize=(16,10)) 
    for i,d,t in zip(range(len(all_data)),all_data,titles):
        ax=plt.subplot(gs[i],projection=ccrs.PlateCarree())
        d=all_data[i]
        img=anomalies(d,var).annual_mean(nyears*12).plotvar(
            ax=ax,
            add_colorbar=False,
            levels=np.linspace(-2,2,50),
            cmap=my.Colormaps.div_tsurf,
            t_student=P(d,var),
            statistics={'value':'all','fs':12}
            )
        ax.set_title(t,fontweight='bold')
    cax=plt.subplot(gs[-1,:])
    plt.colorbar(img,cax=cax,
        orientation='horizontal',
        label='$K$',
        ticks=np.arange(-2,2+0.5,0.5))
    plt.savefig(os.path.join(output_folder,"tsurf"),
        dpi=300,
        bbox_inches='tight')
# plot_tsurf()    

def plot_fig1():
    plt.rcParams.update({'font.size': 11})
    var='air_temperature'
    gs = GridSpec(3, 3, height_ratios=[8,8,1],
                wspace=0.25,hspace=0.3)
    fig=plt.figure(figsize=(16,10)) 
    for i,d,t in zip(range(len(all_data)),all_data,titles):
        ax=plt.subplot(gs[i])
        d=all_data[i]
        img=anomalies(d,var).annual_mean(nyears*12).longitude_mean().plotlev(
            ax=ax,
            add_colorbar=False,
            levels=np.linspace(-2,2,50),
            cmap=my.Colormaps.div_tsurf,
            t_student=P(d,var).longitude_mean(),
            double_axis=True,
            )
        ax.set_title(t,fontweight='bold')
    cax=plt.subplot(gs[-1,:])
    plt.colorbar(img,cax=cax,
        orientation='horizontal',
        label='$K$',
        ticks=np.arange(-2,2+0.5,0.5))
    plt.savefig(os.path.join(output_folder,"fig1_tair"),
        dpi=300,
        bbox_inches='tight')
# plot_fig1() 

def plot_fig2():
    plt.rcParams.update({'font.size': 11})
    var='precipitation_flux'
    gs = GridSpec(3, 3, height_ratios=[8,8,1],
                wspace=0.15,hspace=0)
    fig=plt.figure(figsize=(16,10)) 
    for i,d,t in zip(range(len(all_data)),all_data,titles):
        ax=plt.subplot(gs[i],projection=ccrs.PlateCarree())
        d=all_data[i]
        img=anomalies(d,var).to_mm_per_day().annual_mean(nyears*12).plotvar(
            ax=ax,
            add_colorbar=False,
            levels=np.linspace(-2,2,50),
            cmap=my.Colormaps.div_precip,
            t_student=P(d,var),
            )
        ax.set_title(t,fontweight='bold')
    cax=plt.subplot(gs[-1,:])
    plt.colorbar(img,cax=cax,
        orientation='horizontal',
        label='$mm \cdot d^{-1}$',
        ticks=np.arange(-2,2+0.5,0.5))
    plt.savefig(os.path.join(output_folder,"fig2_precip"),
        dpi=300,
        bbox_inches='tight')
# plot_fig2()  


# PLOT AIR TEMPERATURE ABSOLUTE PROFILES
def plot_airprof():
    f = lambda d: d.air_temperature.annual_mean(nyears*12).global_mean().interp(
        pressure=np.linspace(50,800,1000),method='cubic')

    plt.figure(figsize=(10,6))
    f(ctl).plotprof(
        other_data=[f(z) for z in all_data],
        colors=['blue','red','orange','green','pink','gold','lawngreen'],
        labels=['Control']+titles,
        units='$K$',
        lw=2)
    plt.xlim((200,280))
    plt.ylim(800,50)
    plt.legend()
    plt.title('Air Temperature Profiles')
    plt.savefig(os.path.join(output_folder,'ABS_air_temp_profiles'),bbox_inches='tight',dpi=300)
    plt.show()
    plt.clf()

    f(ctl).plotprof(
        other_data=[f(z) for z in all_data],
        colors=['blue','red','orange','green','pink','gold','lawngreen'],
        labels=['Control']+titles,
        units='$K$',
        lw=2)
    plt.xlim((200,225))
    plt.ylim(250,50)
    plt.legend()
    plt.title('Air Temperature Profiles')
    plt.savefig(os.path.join(output_folder,'ABS_air_temp_profiles_ZOOM'),bbox_inches='tight',dpi=300)
    plt.show()
    plt.clf()
# plot_airprof()


# CIRCULATION STREAMLINES 
anom=lambda x:my.Dataset(x-ctl)
norm_xy=my.DataArray(np.sqrt(anom(co2x4)['x_wind']**2+anom(co2x4)['y_wind']**2))
ax=plt.axes(projection=ccrs.PlateCarree())
anom(co2x4).annual_mean(nyears*12).sel(
    pressure=500, method='nearest').to_continuous_lon().plot.streamplot(
        ax=ax,
        x="longitude_0",
        y="latitude_0",
        u="x_wind",
        v="y_wind",
        density=2,
        linewidth=0.8,
        arrowsize=0.6)
ax.add_feature(cfeature.COASTLINE,facecolor='black',edgecolor='black')

plt.figure()
ax=plt.axes(projection=ccrs.PlateCarree())
norm_xy.sel(
    pressure=500, 
    method='nearest').plotvar(
        ax=ax,
        cmap=my.Colormaps.seq_precip_wet,
        levels=np.linspace(0,6,50),
        du=0.5,)
co2x4.annual_mean().sel(
    pressure=500, 
    method='nearest').plot.streamplot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        x="longitude_0",
        y="latitude_0",
        u="x_wind",
        v="y_wind")    
plt.show()
