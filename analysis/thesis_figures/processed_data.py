import myfuncs as my
import os
import glob
import numpy as np

output_folder="/g/data/w40/dm5220/data/processed_data"
data = glob.glob('/g/data/w40/dm5220/data/*best*') + glob.glob('/g/data/w40/dm5220/data/4co2_fix_tsurf_*_*_*')
data=data[29:]

for d in data:
    ds=my.UM.read_data(d)
    ds.to_netcdf(os.path.join(output_folder,f"{os.path.split(d)[1]}.nc"))
    del ds
