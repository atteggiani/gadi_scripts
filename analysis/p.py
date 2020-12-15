outpath = None
name = "data"
title = None
units = None,
t_student=p
nlev="100"
save_kwargs = None
contourf_kwargs = {"levels":np.linspace(-2,2,100),"cmap":Constants.colormaps.Div_precip}
self = d.annual_mean()

ax = plt.axes() if 'ax' not in contourf_kwargs else contourf_kwargs.pop('ax')
if ('add_colorbar' not in contourf_kwargs):contourf_kwargs['add_colorbar']=True
if contourf_kwargs['add_colorbar']==True:
    if 'cbar_kwargs' not in contourf_kwargs: contourf_kwargs['cbar_kwargs'] = dict()
    if units is not None:
        contourf_kwargs['cbar_kwargs']['label']=units
im=self.plot.contourf(ax=ax,
            yincrease=False,
            **contourf_kwargs,
            )
if isinstance(t_student,bool):
    if t_student:
        raise Exception('t_student must be False, or equal to either a dictionary or an '
                'xarray.DataArray containing t-student distribution probabilities.')
else:
    if check_xarray(t_student,"DataArray"):
        t_student = {"p":t_student}
    elif isinstance(t_student,np.ndarray):
        t_student = {"p":xr.DataArray(data=t_student,dims = ["latitude","longitude"], coords=[Constants.um.latitude,Constants.um.longitude])}
    if isinstance(t_student,dict):
        if "p" not in t_student:
            raise Exception('t_student must be contain "p" key, containing '
                'an xarray.DataArray with t-student distribution '
                'probabilities.\nTo obtain t_student distribution '
                'probabilities, you can use the "t_student_probability" function.')
        elif isinstance(t_student["p"],np.ndarray):
            t_student["p"] = xr.DataArray(data=t_student["p"],dims = ["latitude","longitude"], coords=[Constants.um.latitude,Constants.um.longitude])
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
    DataArray(p.where(p<a,0).where(p>=a,1)).plot.contourf(
                                        yincrease=False,
                                        levels=np.linspace(0,1,3),
                                        hatches=['',t_student['hatches']],
                                        alpha=0,
                                        add_colorbar=False,
                                        )
plt.xlabel("")
plt.xticks(ticks=np.arange(-90,90+30,30),labels=["90S","60S","30S","0","30N","60N","90N"])
plt.gca().xaxis.set_minor_locator(MultipleLocator(10))
plt.tick_params(axis='y',which='minor',left=False,right=False)
plt.tick_params(axis='y',which='major',left=True,right=True)
plt.tick_params(axis='x',which='both',bottom=True,top=True)
plt.title(title)
if save_kwargs is not None:
    save_kwargs = {'dpi':300, 'bbox_inches':'tight', **save_kwargs}
else:
    save_kwargs = {'dpi':300, 'bbox_inches':'tight'}
if outpath is not None:
    plt.savefig(outpath, format = 'png',**save_kwargs)
return im