import myfuncs as my
from  multiprocessing import Pool,cpu_count
import glob
from gc import collect
import sys

input_folder=sys.argv[1]
ncpus = cpu_count()
files = glob.glob(input_folder+'/*')
# data_vars=['change_over_time_in_air_temperature_due_to_stratiform_precipitation',
#            'change_over_time_in_air_temperature_due_to_convection']

def convert(file):
    # Convert the netCDF output from model levels to pressure levels
    my.load_dataset(file).to_pressure_lev(data_vars=None).to_netcdf(file,mode='w')
    return file
# for file in files:
#     convert(file)
def main(files):
    '''
    Function to parallelise the conversion to netCDF
    '''
    with Pool(processes=ncpus) as p:
        p.map(convert,files)
        p.close()
        p.join()  

if __name__ == '__main__':
    main(files)
    collect()