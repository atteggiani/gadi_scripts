from argparse import ArgumentParser
from myfuncs import UM
import myfuncs as my
import iris
import os
from  multiprocessing import Pool,cpu_count
import numpy as np
import glob
from gc import collect

# Argument parsing
parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,default="/scratch/w40/dm5220/umui")
parser.add_argument('-o','--output',type=str)
parser.add_argument('--id','--exp_id',type=str)
parser.add_argument('--ncpus',type=int)
args=parser.parse_args()

input_folder=args.input
output_folder=args.output
exp_id=args.id
ncpus=args.ncpus
if exp_id is None: input_folder,exp_id = os.path.split(input_folder)
if output_folder is None: output_folder = f"/g/data3/w40/dm5220/data/{exp_id}"
if ncpus is None: ncpus = cpu_count()


ind=len(exp_id)+4
# Look inside the um output folder to get the years of the run
years=list(set([os.path.split(x)[1][ind:-2] for x in \
    glob.glob(os.path.join(input_folder,exp_id,"{}a@pa*".format(exp_id)))]))
streams=["a","c"]
all_years=years*len(streams)
all_streams=np.repeat(streams,len(years))
os.makedirs(output_folder,exist_ok=True)

def print_callback(result):
    print(f"Completed processing {result}")

def convert(stream,year):
    '''
    Function to convert the um output to netcdf
    '''
    outfile=os.path.join(output_folder,f"{exp_id}_p{stream}{UM.from_um_filename_years(year)}.nc")
    try:
        x=iris.load(os.path.join(input_folder,exp_id,f"{exp_id}a@p{stream}{year}*"))
        iris.save(x,outfile)
        del x
        collect()
        # Convert the netCDF output from model levels to pressure levels
        print(f"Convert to pressure levels year {year}")
        my.load_dataset(outfile).to_pressure_lev().to_netcdf(outfile,mode='w')
        return outfile
    except OSError as e:
        return e


def main(streams,years):
    '''
    Function to parallelise the conversion to netCDF
    '''
    p=Pool(processes=ncpus)
    for s,y in zip(streams,years):
        p.apply_async(convert,args=(s,y),
            callback=print_callback)
    p.close()
    p.join()  

if __name__ == '__main__':
    main(all_streams,all_years)
