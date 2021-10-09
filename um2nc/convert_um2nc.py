import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
from myfuncs import UM,Dataset
import myfuncs as my
import xarray as xr
import iris
import os
from  multiprocessing import Pool,cpu_count
from itertools import repeat
import numpy as np
import glob
import time

# Argument parsing
parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,default="/scratch/w48/dm5220/umui")
parser.add_argument('-o','--output',type=str)
parser.add_argument('--id','--exp_id',type=str)
parser.add_argument('--ncpus',type=int)
args=parser.parse_args()

input_folder=args.input
output_folder=args.output
exp_id=args.id
ncpus=args.ncpus
if exp_id is None: input_folder,exp_id = os.path.split(input_folder)
if ncpus is None: ncpus = cpu_count()


ind=len(exp_id)+4
# Look inside the um output folder to get the years of the run
years=list(set([os.path.split(x)[1][ind:-2] for x in glob.glob(os.path.join(input_folder,exp_id,"{}a@pa*".format(exp_id)))]))
# streams=["a","c","e"]
streams=["a"]
os.makedirs(output_folder,exist_ok=True)

def convert(input_folder,output_folder,exp_id,year):
    '''
    Function to convert the um output to netcdf
    '''
    for s in streams:
        outfile=os.path.join(output_folder,f"{exp_id}_p{s}{UM.from_um_filename_years(year)}.nc")
        x=iris.load(os.path.join(input_folder,exp_id,f"{exp_id}a@p{s}{year}*"))  
        iris.save(x,outfile)

def to_pressure_levels(output_folder,exp_id,year):
    '''
    Function to convert the netCDF output from model
    levels to pressure levels.
    '''
    for s in streams:
        file=os.path.join(output_folder,f"{exp_id}_p{s}{UM.from_um_filename_years(year)}.nc")
        my.load_dataset(file).to_pressure_lev().to_netcdf(file,mode='w')
    
def main(input_folder,output_folder,exp_id,years):
    '''
    Function to parallelise the conversion process
    '''
    p=Pool(processes=ncpus)
    p.starmap(convert,zip(repeat(input_folder),repeat(output_folder),repeat(exp_id),years))
    p.close()
    p.join()  

def main_2(output_folder,exp_id,years):
    '''
    Function to parallelise the conversion process
    '''
    p=Pool(processes=ncpus)
    p.starmap(to_pressure_levels,zip(repeat(output_folder),repeat(exp_id),years))
    p.close()
    p.join() 

if __name__ == '__main__':
    main(input_folder,output_folder,exp_id,years)
    main_2(output_folder,exp_id,years)
    
