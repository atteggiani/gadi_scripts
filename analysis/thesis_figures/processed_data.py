import myfuncs as my
from multiprocessing import Pool
import os
import glob
import numpy as np

output_folder="/g/data/w40/dm5220/data/processed_data"
data = glob.glob('/g/data/w40/dm5220/data/*best*') + glob.glob('/g/data/w40/dm5220/data/4co2_fix_tsurf_*_*_*')

def convert(d):
    ds=my.UM.read_data(d)
    ds.to_netcdf(os.path.join(output_folder,os.path.split(d)[1]))

if __name__ == "__main__":
    with Pool() as p:
        p.map(convert,data)
        