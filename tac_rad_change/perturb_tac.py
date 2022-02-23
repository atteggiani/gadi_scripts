import myfuncs as my
import sys
import os

file=sys.argv[1]
# file='/g/data/w48/dm5220/ancil/user_mlevel/tac_rad_change/files_for_xancil/m_equa_la.nc'
newfile=os.path.splitext(file)[0]+'_p.nc'
a=my.open_dataarray(file)
b=a*.9999
b.to_netcdf(newfile)