#%%
import warnings
warnings.simplefilter("ignore")
from myfuncs import *

#%%
def get_data(data,var,a=1,mean=None,anom=True,fun=None):
    # Get only first 20 years of simulation
    data=data.isel(time=slice(0,240))
    ctl=data_ctl.isel(time=slice(0,240))
    if fun is not None: 
        data = fun(data)
        data_control = DataArray(fun(ctl)[var].chunk({"time":20})*a)
    else:    
        data_control = DataArray(ctl[var].chunk({"time":20})*a)
        
    data = DataArray(data[var].chunk({'time':10})*a)
    if mean == "lon":
        lon=data.get_spatial_coords()[1]
        data_control=data_control.mean(lon)
        data=data.mean(lon)
    elif (mean == "pressure") and ("pressure" in data.dims):
        data_control=data_control.mean("pressure")
        data=data.mean("pressure")
    p_amean=data.t_student_probability(data_control)
    p_JJA=data.t_student_probability(data_control,season="JJA")
    p_DJF=data.t_student_probability(data_control,season="DJF")
    if anom: data = data - data_control
    data=data.groupby("time.season").mean("time")
    data_JJA=data.sel(season="JJA")
    data_DJF=data.sel(season="DJF")
    data_amean=data.mean("season")
    return {'data':{"JJA":data_JJA,"DJF":data_DJF,"amean":data_amean},'p':{"JJA":p_JJA,"DJF":p_DJF,"amean":p_amean}}

def plot_levels(data,var,min=None,max=None,du=1,a=1,
                title="",units="",outpath=None,ttest=False,fun=None,**kwargs):
    def plot_(data,min=min,max=max,**kwargs):
        if (min is not None) and (max is not None):
            levels=np.linspace(min,max,100)
            norm = colors.DivergingNorm(vmin=min,vcenter=0,vmax=max)
        else:
            levels=None
            norm=None
        im=data.plotlev(levels = levels,
                        norm=norm,
                        add_colorbar=False,
                        ylim=[1000,50],
                        yscale="log",
                        **kwargs,
                        )
        plt.yticks(ticks=[1000,800,600,400,200,50],labels=["1000","800","600","400","200","50"])
        return im
    
    if (min is not None) and (max is not None) and (du is not None):
        ticks=np.arange(min,max+du,du)
    else: 
        ticks=None
    
    d=get_data(data,var,a,mean="lon",fun=fun)

    fig = plt.figure(figsize=(16,4.8),constrained_layout=False)
    wspace=0.3; hspace=0.2; ncols=3; nrows=1
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         wspace=wspace, hspace=hspace,
                         bottom=0.15, top=0.85)
    gs2=fig.add_gridspec(ncols=12, nrows=1,
                         bottom=0, top=0.06)

    ax1 = fig.add_subplot(gs1[0, 0])
    if ttest:
        im=plot_(d["data"]["DJF"],ax=ax1,min=min,max=max,t_student=d["p"]["DJF"],**kwargs)
    else:
        im=plot_(d["data"]["DJF"],ax=ax1,min=min,max=max,**kwargs)
    plt.title("DJF mean",fontsize=14)
    ax2 = fig.add_subplot(gs1[0, 1])
    if ttest:
        plot_(d["data"]["JJA"],ax=ax2,min=min,max=max,t_student=d["p"]["JJA"],**kwargs)
    else:
        plot_(d["data"]["JJA"],ax=ax2,min=min,max=max,**kwargs)
    plt.title("JJA mean",fontsize=14)
    ax3 = fig.add_subplot(gs1[0, 2])
    if ttest:
        plot_(d["data"]["amean"],ax=ax3,min=min,max=max,t_student=d["p"]["amean"],**kwargs)
    else:
        plot_(d["data"]["amean"],ax=ax3,min=min,max=max,**kwargs)
    plt.title("Annual mean",fontsize=14)
    axc1 = fig.add_subplot(gs2[0, 1:-1])
    plt.colorbar(im,cax=axc1, orientation='horizontal',
                 ticks=ticks)
    plt.text(1.03,0.5, "[{}]".format(units),verticalalignment="center",fontsize=12,
             transform=axc1.transAxes)

    plt.suptitle(title,fontsize=16)
    if outpath is not None:
        plt.savefig(os.path.join(output_folder,outpath),dpi=300,bbox_inches="tight")

def plot_levels_zoom(data,var,min=None,max=None,du=1,a=1,
                title="",units="",outpath=None,ttest=False,fun=None,**kwargs):
    def plot_(data,min=min,max=max,**kwargs):
        if (min is not None) and (max is not None):
            levels=np.linspace(min,max,100)
            norm=colors.DivergingNorm(vmin=min,vcenter=0,vmax=max)
        else:
            levels=None
            norm=None
            
        im=data.plotlev(levels = levels,
                        norm = norm,
                        add_colorbar=False,
                        ylim=[1000,800],
                        **kwargs,
                        )
        plt.ylim([1000,800])
        plt.yticks(ticks=[1000,900,800],labels=["1000","900","800"])
        return im
    
    if (min is not None) and (max is not None) and (du is not None):
        ticks=np.arange(min,max+du,du)
    else: 
        ticks=None
    
    d=get_data(data,var,a,mean="lon",fun=fun)
    
    fig = plt.figure(figsize=(16,4.8),constrained_layout=False)
    wspace=0.3; hspace=0.2; ncols=3; nrows=1
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         wspace=wspace, hspace=hspace,
                         bottom=0.15, top=0.85)
    gs2=fig.add_gridspec(ncols=12, nrows=1,
                         bottom=0, top=0.06)

    ax1 = fig.add_subplot(gs1[0, 0])
    if ttest:
        im=plot_(d["data"]["DJF"],ax=ax1,min=min,max=max,t_student=d["p"]["DJF"],**kwargs)
    else:
        im=plot_(d["data"]["DJF"],ax=ax1,min=min,max=max,**kwargs)
    plt.title("DJF mean",fontsize=14)
    ax2 = fig.add_subplot(gs1[0, 1])
    if ttest:
        plot_(d["data"]["JJA"],ax=ax2,min=min,max=max,t_student=d["p"]["JJA"],**kwargs)
    else:
        plot_(d["data"]["JJA"],ax=ax2,min=min,max=max,**kwargs)
    plt.title("JJA mean",fontsize=14)
    ax3 = fig.add_subplot(gs1[0, 2])
    if ttest:
        plot_(d["data"]["amean"],ax=ax3,min=min,max=max,t_student=d["p"]["amean"],**kwargs)
    else:
        plot_(d["data"]["amean"],ax=ax3,min=min,max=max,**kwargs)
    plt.title("Annual mean",fontsize=14)
    axc1 = fig.add_subplot(gs2[0, 1:-1])
    plt.colorbar(im,cax=axc1, orientation='horizontal',
                 ticks=ticks)
    plt.text(1.03,0.5, "[{}]".format(units),verticalalignment="center",fontsize=12,
             transform=axc1.transAxes)

    plt.suptitle(title,fontsize=16)
    if outpath is not None:
        plt.savefig(os.path.join(output_folder,outpath),dpi=300,bbox_inches="tight")
        
def plot_patterns(data,var,min=None,max=None,du=1,a=1,
                title="",units="",outpath=None,ttest=False,fun=None,**kwargs):
    def plot_(data,min=min,max=max,**kwargs):
        if (min is not None) and (max is not None):
            levels=np.linspace(min,max,100)
            norm=colors.DivergingNorm(vmin=min,vcenter=0,vmax=max)
        else:
            levels=None
            norm=None
        return data.plotvar(
                        levels = levels,
                        norm=norm,
                        add_colorbar=False,
                        **kwargs,
                        )    
    
    
    if (min is not None) and (max is not None) and (du is not None):
        ticks=np.arange(min,max+du,du)
    else: 
        ticks=None
    
    mean = "pressure" if "pressure" in data_ctl[var].dims else None
    d=get_data(data,var,a,mean=mean,fun=fun)
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    wspace=0.3; hspace=0.2; ncols=3; nrows=1
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         wspace=wspace, hspace=hspace,
                         bottom=0.15, top=0.85)
    gs2=fig.add_gridspec(ncols=12, nrows=1,
                         bottom=0, top=0.06)
    
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    if ttest:
        im=plot_(d["data"]["DJF"],ax=ax1,min=min,max=max,t_student=d["p"]["DJF"],**kwargs)
    else:
        im=plot_(d["data"]["DJF"],ax=ax1,min=min,max=max,**kwargs)
    plt.title("DJF mean",fontsize=14)
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    if ttest:
        plot_(d["data"]["JJA"],ax=ax2,min=min,max=max,t_student=d["p"]["JJA"],**kwargs)
    else:
        plot_(d["data"]["JJA"],ax=ax2,min=min,max=max,**kwargs)
    plt.title("JJA mean",fontsize=14)
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    if ttest:
        plot_(d["data"]["amean"],ax=ax3,min=min,max=max,t_student=d["p"]["amean"],**kwargs)
    else:
        plot_(d["data"]["amean"],ax=ax3,min=min,max=max,**kwargs)
    plt.title("Annual mean",fontsize=14)
    axc1 = fig.add_subplot(gs2[0, 1:-1])
    plt.colorbar(im,cax=axc1, orientation='horizontal',
                 ticks=ticks)
    plt.text(1.03,0.5, "[{}]".format(units),verticalalignment="center",fontsize=12,
             transform=axc1.transAxes)
    plt.suptitle(title,fontsize=16)
    if outpath is not None:
        plt.savefig(os.path.join(output_folder,outpath),dpi=300,bbox_inches="tight")
        
def plot_amean_lev(data,var,a=1,title=None,outpath=None,min=None,max=None,du=1,units=None,fun=None,anom=True,**kwargs):
    d=get_data(data,var,a,mean="lon",fun=fun,anom=anom)
    d=d['data']['amean']
    if (min is not None) and (max is not None) and (du is not None):
        cbar_kwargs={'ticks':np.arange(min,max+du,du)}
        levels = np.linspace(min,max,100)
        norm=colors.DivergingNorm(vmin=min,vcenter=0,vmax=max)
    else:
        cbar_kwargs=dict()
        levels=None
        norm=None
    if units is not None:
        cbar_kwargs['label']=units
    if 'ttest' in kwargs:
        if kwargs.pop('ttest'):
            kwargs['t_student']=d['p']['amean']
    d.plotlev(levels=levels,
        norm=norm,
        ylim=[1000,50],
        yscale="log",
        cbar_kwargs=cbar_kwargs,
        **kwargs)
    plt.yticks(ticks=[1000,800,600,400,200,50],labels=["1000","800","600","400","200","50"])
    if title is None: title = d.name
    plt.title(title)
    if outpath is not None:
        plt.savefig(os.path.join(output_folder,outpath),dpi=300,bbox_inches="tight")

def plot_amean_pat(data,var,a=1,title=None,outpath=None,min=None,max=None,du=1,units=None,anom=True,fun=None,**kwargs):
    mean = "pressure" if "pressure" in data_ctl[var].dims else None
    d=get_data(data,var,a,mean=mean,fun=fun,anom=anom)
    d=d['data']['amean']
    if (min is not None) and (max is not None) and (du is not None):
        cbar_kwargs={'ticks':np.arange(min,max+du,du)}
        levels = np.linspace(min,max,50)
        norm=colors.DivergingNorm(vmin=min,vcenter=0,vmax=max)
    else:
        cbar_kwargs=dict()
        levels=None
        norm=None
    if units is not None:
        cbar_kwargs['label']=units
    if 'ttest' in kwargs:
        if kwargs.pop('ttest'):
            kwargs['t_student']=d['p']['amean']
    d.plotvar(levels = levels,
        norm = norm,
        cbar_kwargs=cbar_kwargs,
        **kwargs)
    if title is None: title = d.name
    plt.title(title)
    if outpath is not None:
        plt.savefig(os.path.join(output_folder,outpath),dpi=300,bbox_inches="tight")

#%%
input_folder="/g/data/w48/dm5220/data"
output_folder=input_folder+"/figures/analysis"
alpha_precip=86400

#DATA
data_ctl = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control/vabva_pa*.nc"),
                  concat_dim="time",parallel=True))
data_4co2 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2/vabvb_pa*.nc"),
                  concat_dim="time",parallel=True))
data_4co2_fix_ctl = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_tsurf/vabvc_pa*.nc"),
                  concat_dim="time",parallel=True))
# data_ctl_fix_4co2 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_4co2_tsurf/vabvd_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_ctl_fix_ctl_greb = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_control.greb_tsurf/vabvf_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_4co2_fix_4co2_greb = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_4co2.greb_tsurf/vabvg_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_4co2_fix_LAND_ctl = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_LAND_temp/vabvh_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_4co2_fix_SST_ctl = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_pres_control_SST/vabvi_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_ctl_fix_LAND_4co2 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_4co2_LAND_temp/vabvj_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_ctl_fix_SST_4co2 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_4co2_SST/vabvk_pa*.nc"),
#                   concat_dim="time",parallel=True))
# data_ctl_fix_ctl_evap_sea_x085 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_control_evap_sea_x0.85/vabvl_pa*.nc"),
#                             concat_dim="time",parallel=True))
# data_ctl_fix_ctl_evap_x085 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_control_evap_x0.85/vabvn_pa*.nc"),
#                             concat_dim="time",parallel=True))
# data_ctl_solar_pl50 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_solar_plus50W/vabvo_pa*.nc"),
#                             concat_dim="time",parallel=True))
data_ctl_fix_ctl_solar_pl50 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"control_pres_control_solar_plus50W/vabvp_pa*.nc"),
                            concat_dim="time",parallel=True))
data_4co2_solar_mi50 = add_evaporation(xr.open_mfdataset(os.path.join(input_folder,"4co2_solar_minus50W/vabvq_pa*.nc"),
                              concat_dim="time",parallel=True))

#%%
# ( DATA , TITLE , OUT_NAME )
# datas=[
#        (data_4co2, "4co2" , "4co2"),
#        (data_4co2_fix_ctl , "4co2 + fixed control tsurf" , "4co2_fix_ctl"),
#        (data_ctl_fix_ctl_solar_pl50 , "control + fixed control + solar +50 W/m2" , "ctl_fix_ctl_solar_pl50"),
#        (data_4co2_solar_mi50 , "4co2 + solar -50 W/m2" , "4co2_solar_mi50")]       
#        (data_ctl_fix_4co2 , "control + fixed 4co2 tsurf" , "ctl_fix_4co2"),       
#        (data_ctl_fix_ctl_greb , "control + fixed control tsurf + GREB" , "ctl_fix_ctl_greb"),
#        (data_4co2_fix_4co2_greb , "4co2 + fixed 4co2 tsurf + GREB" , "4co2_fix_4co2_greb"),
#        (data_4co2_fix_LAND_ctl , "4co2 + fixed control LAND" , "4co2_fix_ctl_LAND"),
#        (data_4co2_fix_SST_ctl , "4co2 + fixed control SST" , "4co2_fix_ctl_SST"),
#        (data_ctl_fix_LAND_4co2 , "control + fixed 4co2 LAND" , "ctl_fix_4co2_LAND"),
#        (data_ctl_fix_SST_4co2 , "control + fixed 4co2 SST" , "ctl_fix_4co2_SST"),
#        (data_ctl_fix_ctl_evap_sea_x085 , "control + fixed control tsurf + evap sea 0.85" , "ctl_fix_ctl_evap_sea_x0.85"),
#        (data_ctl_fix_ctl_evap_x085 , "control + fixed control tsurf + evap 0.85" , "ctl_fix_ctl_evap_x0.85"),
#        (data_ctl_solar_pl50 , "control + solar +50 W/m2" , "ctl_solar_pl50")]

#%%
#SINGLE FIGURES
exp_ = ["4co2","control + fixed 4co2 tsurf" , "control + fixed 4co2 SST" , "4co2 + fixed 4co2 tsurf + GREB",
        "control + solar +50 W/m2"]
for d,t,o in datas:
    m,mm = (-6,6) if t in exp_ else (-3,3)
#SURFACE TEMPERATURE
    var="surface_temperature"
    tit ="Surface temperature"
    outvar="surf_temp"
    plt.figure()
    plot_amean_pat(data=d,var=var,
        min=m,max=mm,
        title = "{} - {}".format(tit,t),
        units = "°C",
        ttest=True,
        outpath = "{}_{}_pat_amean.png".format(outvar,o),
        cmap = Constants.colormaps.div_tsurf)

#AIR TEMPERATURE
    var="air_temperature"
    tit ="Air temperature"
    outvar="air_temp"
    plt.figure()
    plot_levels(data=d,var=var,
        min=m,max=mm,
        title = "{} - {}".format(tit,t),
        units = "°C",
        ttest=True,
        outpath = "{}_{}_lev.png".format(outvar,o),
        cmap = Constants.colormaps.div_tsurf)
    plt.figure()
    plot_amean_lev(data=d,var=var,
        min=m,max=mm,
        title = "{} - {}".format(tit,t),
        units = "°C",
        ttest=True,
        outpath = "{}_{}_lev_amean.png".format(outvar,o),
        cmap = Constants.colormaps.div_tsurf)

#PRECIPITATION
    var="precipitation_flux"
    tit ="Precipitation"
    outvar="precip"
    plt.figure()
    plot_patterns(data=d,var=var,
        a=alpha_precip,
        min=-2,max=2,du=0.5,
        title = "{} - {}".format(tit,t),
        units = "mm/day",
        ttest=True,
        outpath = "{}_{}_pat.png".format(outvar,o),
        cmap = Constants.colormaps.div_precip)
    plt.figure() 
    plot_amean_pat(data=d,var=var,
        a=alpha_precip,
        min=-2,max=2,du=0.5,
        title = "{} - {}".format(tit,t),
        units = "mm/day",
        ttest=True,
        outpath = "{}_{}_pat_amean.png".format(outvar,o),
        cmap = Constants.colormaps.div_precip)

# #HUMIDITY
#     var="relative_humidity"
#     tit ="Relative humidity"
#     outvar="humidity"
#     plt.figure()  
#     plot_patterns(data=d,var=var,
#         min=-10,max=10,du=2.5,
#         title = "{} - {}".format(tit,t),
#         units = "%",
#         outpath = "{}_{}_pat.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)
#     plt.figure()
#     plot_amean_pat(data=d,var=var,
#         min=-10,max=10,du=2.5,
#         title = "{} - {}".format(tit,t),
#         units = "%",
#         outpath = "{}_{}_pat_amean.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)

# #AIR SPEED
#     var="upward_air_velocity"
#     tit ="Up air speed"
#     outvar="air_speed"
#     plt.figure()
#     plot_patterns(data=d,var=var,
#         units="m/s",
#         min=-0.005,max=0.005,du=0.001,
#         title = "{} - {}".format(tit,t),
#         outpath = "{}_{}_pat.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip,
#         fun=lambda x: x.sel(pressure=slice(199,1001)))
#     plt.figure()
#     plot_amean_pat(data=d,var=var,
#         units="m/s",
#         min=-0.005,max=0.005,du=0.001,
#         title = "{} - {}".format(tit,t),
#         outpath = "{}_{}_pat_amean.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip,
#         fun=lambda x: x.sel(pressure=slice(199,1001)))

#     plt.figure()
#     plot_levels(data=d,var=var,
#         units="m/s",
#         min=-0.001,max=0.001,du=0.00025,
#         title = "{} - {}".format(tit,t),
#         outpath = "{}_{}_lev.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)
#     plt.figure()
#     plot_amean_lev(data=d,var=var,
#         units="m/s",
#         min=-0.001,max=0.001,du=0.00025,
#         title = "{} - {}".format(tit,t),
#         outpath = "{}_{}_lev_amean.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)
    
# # EVAPORATION SEA
#     var="evaporation_flux_from_open_sea"
#     tit ="Evaporation (sea)"
#     outvar="evap_sea"
#     plt.figure()
#     plot_patterns(data=d,var=var,
#         a=alpha_precip,
#         min=-1,max=1,du=0.2,
#         title = "{} - {}".format(tit,t),
#         units = "mm/day",
#         outpath = "{}_{}_pat.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)
#     plt.figure() 
#     plot_amean_pat(data=d,var=var,
#         a=alpha_precip,
#         min=-1,max=1,du=0.2,
#         title = "{} - {}".format(tit,t),
#         units = "mm/day",
#         outpath = "{}_{}_pat_amean.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)

# # EVAPORATION LAND
#     var="evaporation_from_soil_surface"
#     tit ="Evaporation (land)"
#     outvar="evap_land"
#     plt.figure()
#     plot_patterns(data=d,var=var,
#         a=alpha_precip,
#             min=-1,max=1,du=0.2,
#         title = "{} - {}".format(tit,t),
#         units = "mm/day",
#         outpath = "{}_{}_pat.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)
#     plt.figure() 
#     plot_amean_pat(data=d,var=var,
#         a=alpha_precip,
#             min=-1,max=1,du=0.2,
#         title = "{} - {}".format(tit,t),
#         units = "mm/day",
#         outpath = "{}_{}_pat_amean.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)

# # EVAPORATION
#     var="evaporation"
#     tit ="Evaporation"
#     outvar="evap"
#     plt.figure()
#     plot_patterns(data=d,var=var,
#         a=alpha_precip,
#             min=-1,max=1,du=0.2,
#         title = "{} - {}".format(tit,t),
#         units = "mm/day",
#         outpath = "{}_{}_pat.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)
#     plt.figure() 
#     plot_amean_pat(data=d,var=var,
#         a=alpha_precip,
#             min=-1,max=1,du=0.2,
#         title = "{} - {}".format(tit,t),
#         units = "mm/day",
#         outpath = "{}_{}_pat_amean.png".format(outvar,o),
#         cmap = Constants.colormaps.Div_precip)

#%% DIFFERENCES
output_folder_diff = os.path.join(output_folder,"differences")

# data_4co2_fix_ctl - data_ctl_fix_ctl_solar_pl50
data1=data_4co2_fix_ctl
data2=data_ctl_fix_ctl_solar_pl50
#TSURF
var="surface_temperature"
d = DataArray(data1[var]-data2[var])
p = DataArray(data1[var]).t_student_probability(data2[var])  
plt.figure()
d.annual_mean(240).plotvar(
          cmap = Constants.colormaps.div_tsurf,
          levels = np.linspace(-2,2,100),
          cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5)},
#           norm = colors.DivergingNorm(vmin=-1,vcenter=0,vmax=2),
          t_student=p,
          title = "(4co2 fix) - (fix sol50+) | Surface Temperature",
          units = "°C",
          outpath = os.path.join(output_folder_diff,"diff_4co2fix_fixs50p_tsurf.png"))

#TAIR
var="air_temperature"
d = DataArray(data1[var].mean("longitude_0") - data2[var].mean("longitude_0"))
p = DataArray(data1[var].mean("longitude_0")).t_student_probability(data2[var].mean("longitude_0"))
plt.figure()
d.annual_mean(240).plotlev(
          cmap = Constants.colormaps.div_tsurf,
          levels = np.linspace(-2,2,100),
          cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5)},
#           norm = colors.DivergingNorm(vmin=-1,vcenter=0,vmax=2),
          t_student=p,
          title = "(4co2 fix) - (fix sol50+) | Air Temperature",
          units = "°C",
          outpath = os.path.join(output_folder_diff,"diff_4co2fix_fixs50p_tair.png"))

# data_4co2_fix_ctl - data_4co2_solar_mi50
data1=data_4co2_fix_ctl
data2=data_4co2_solar_mi50
#TSURF
var="surface_temperature"
d = DataArray(data1[var]-data2[var])
p = DataArray(data1[var]).t_student_probability(data2[var]) 
plt.figure()
d.annual_mean(240).plotvar(
          cmap = Constants.colormaps.div_tsurf,
          levels = np.linspace(-2,2,100),
          cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5)},
#           norm = colors.DivergingNorm(vmin=-1,vcenter=0,vmax=2),
          t_student=p,
          title = "(4co2 fix) - (4co2 sol50-) | Surface Temperature",
          units = "°C",
          outpath = os.path.join(output_folder_diff,"diff_4co2fix_4co2s50m_tsurf.png"))

#TAIR
var="air_temperature"
d = DataArray(data1[var].mean("longitude_0") - data2[var].mean("longitude_0"))
p = DataArray(data1[var].mean("longitude_0")).t_student_probability(data2[var].mean("longitude_0")) 
plt.figure()
d.annual_mean(240).plotlev(
          cmap = Constants.colormaps.div_tsurf,
          levels = np.linspace(-2,2,100),
          cbar_kwargs={"ticks":np.arange(-2,2+0.5,0.5)},
#           norm = colors.DivergingNorm(vmin=-1,vcenter=0,vmax=2),
          t_student=p,
          title = "(4co2 fix) - (4co2 sol50-) | Air Temperature",
          units = "°C",
          outpath = os.path.join(output_folder_diff,"diff_4co2fix_4co2s50m_tair.png"))


# %%
#VERTICAL PROFILES

