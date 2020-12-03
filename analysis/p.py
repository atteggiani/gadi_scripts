projection = None
outpath = None
name = "data"
title = "Difference 4co2 and solar +50W - Precipitation",
statistics=True
t_student=p1
nlev="100"
coast_kwargs = None
land_kwargs = None
save_kwargs = None
contourf_kwargs = {"levels":np.linspace(-2,2,100),"cmap":Constants.colormaps.Div_precip}
self = DataArray(d).annual_mean()

def _get_var(x):
    keys = x.attrs.keys()
    name = x.name if x.name is not None else 'data'
    if 'long_name' in keys:
        title = x.attrs['long_name'] if x.attrs['long_name'] is not None else ''
    else:
        title = x.name if x.name is not None else ''
    if 'units' in keys:
        units = x.attrs['units'] if x.attrs['units'] is not None else ''
    else:
        units = ''
    if 'annual_mean' in keys:
        title = title + ' Annual Mean'
        name=name+'.amean'
    if 'seasonal_cycle' in keys:
        title = title + ' Seasonal Cycle'
        name=name+'.seascyc'
        cmap = cm.RdBu_r
    if 'anomalies' in keys:
        title = title + ' Anomalies'
        name=name+'.anom'
    return title,name,units

param=self._get_param(nlev=nlev)
self=param['self']
if title is None: title = _get_var(self)[0]
if name is None: name = _get_var(self)[1]
if nlev is None: nlev=100
units = _get_var(self)[2]

new_contourf_kwargs = contourf_kwargs
if projection is None: projection = ccrs.Robinson()
elif not projection: projection = ccrs.PlateCarree()
if 'ax' not in contourf_kwargs:
    new_contourf_kwargs['ax'] = plt.axes(projection=projection)
if 'cmap' not in contourf_kwargs:
    new_contourf_kwargs['cmap'] = param['cmap']
if ('levels' not in contourf_kwargs) and ('norm' not in contourf_kwargs):
    if param['levels'] is None:
        new_contourf_kwargs['levels'] = nlev
    else:
        new_contourf_kwargs['levels'] = param['levels']
if ('add_colorbar' not in contourf_kwargs):contourf_kwargs['add_colorbar']=True
if contourf_kwargs['add_colorbar']==True:
    cbar_kwargs = {'orientation':'horizontal', 'label':units}
    if 'cbar_kwargs' in contourf_kwargs:
        cbar_kwargs.update(contourf_kwargs['cbar_kwargs'])
    if ('ticks' not in cbar_kwargs):
        cbar_kwargs['ticks'] = param['cbticks']
    new_contourf_kwargs['cbar_kwargs']=cbar_kwargs

if land_kwargs is not None:
    land_kwargs = {'edgecolor':'face', 'facecolor':'black', **land_kwargs}
else:
    land_kwargs = {'edgecolor':'face', 'facecolor':'black'}

if coast_kwargs is not None:
    coast_kwargs = {**coast_kwargs}
else:
    coast_kwargs = {}
if self.name == 'cloud':
    coast_kwargs = {'edgecolor':[0,.5,0.3],**coast_kwargs}

if save_kwargs is not None:
    save_kwargs = {'dpi':300, 'bbox_inches':'tight', **save_kwargs}
else:
    save_kwargs = {'dpi':300, 'bbox_inches':'tight'}

self._to_contiguous_lon().plot.contourf(transform=ccrs.PlateCarree(),**new_contourf_kwargs)

plt.gca().add_feature(cfeature.COASTLINE,**coast_kwargs)
if (self.name == 'tocean'):
    plt.gca().add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m'),
                            **land_kwargs)
if statistics:
    txt = ('gmean = {:.3f}'+'\n'+'rms = {:.3f}').format(self.global_mean().values,self.rms().values)
    plt.text(1.05,1,txt,verticalalignment='top',horizontalalignment='right',
                transform=plt.gca().transAxes,fontsize=6)
if isinstance(t_student,bool):
    if t_student:
        raise Exception('t_student must be False, or equal to either a dictionary or an '
                'xarray.DataArray containing t-student distribution probabilities.')
else:
    if check_xarray(t_student,"DataArray"):
        _check_shapes(t_student,self)
        t_student = {"p":t_student}
    elif isinstance(t_student,np.ndarray):
        t_student = {"p":xr.DataArray(data=t_student,dims = ["latitude","longitude"], coords=[Constants.um.latitude,Constants.um.longitude])}
    if isinstance(t_student,dict):
        if "p" not in t_student:
            raise Exception('t_student must be contain "p" key, containing '
                'an xarray.DataArray with t-student distribution '
                'probabilities.\nTo obtain t_student distribution '
                'probabilities, you can use the "t_student_probability" function.')
        if "treshold" in t_student:
            if t_student["treshold"] > 1:
                raise Exception("Treshold must be <= 1")
        else:
            t_student["treshold"]=0.05
        if "hatches" not in t_student:
            t_student["hatches"]= '///'
    else:
        raise Exception('t_student must be either a dictionary or an '
                'xarray.DataArray containing t-student distribution probabilities.')
    p=t_student["p"]
    a=t_student["treshold"]
    DataArray(p.where(p<a,0).where(p>=a,1))._to_contiguous_lon().plot.contourf(
                                        ax=new_contourf_kwargs['ax'],
                                        transform=ccrs.PlateCarree(),
                                        hatches=[t_student['hatches']],
                                        alpha=0,
                                        add_colorbar=False,
                                        )
plt.title(title)
if outpath is not None:
    plt.savefig(outpath, format = 'png',**save_kwargs)
    # plt.close()
return im