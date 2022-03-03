import myfuncs as my
import sys
import os

file=sys.argv[1]
pval=float(sys.argv[2])
newfile=os.path.splitext(file)[0]+'_p.nc'
a=my.open_dataarray(file)
b=a*pval
b.to_netcdf(newfile)