#!/g/data3/hh5/public/apps/miniconda3/envs/analysis3-20.10/bin/python3
import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser

parser=ArgumentParser()
parser.add_argument('-i','--input',type=str,default="/scratch/w48/dm5220/umui")
parser.add_argument('-o','--output',type=str)
parser.add_argument('--id','--exp_id',type=str)
parser.add_argument('--ncpus',type=int)
args=parser.parse_args()

from myfuncs import Constants
import iris
import os
from  multiprocessing import Pool,cpu_count
from itertools import repeat
import numpy as np
import glob

input_folder=args.input
output_folder=args.output
exp_id=args.id
ncpus=args.ncpus
if exp_id is None: input_folder,exp_id = os.path.split(input_folder)
if ncpus is None: ncpus = cpu_count()

ind=len(exp_id)+4
years=set([os.path.split(x)[1][ind:-2] for x in glob.glob(os.path.join(input_folder,exp_id,"{}a@pa*".format(exp_id)))])
os.makedirs(output_folder)

def convert(input_folder,exp_id,year,output_folder):
    streams=Constants.um.streams()
    # for s in streams:
        # try:
        #     x=iris.load(os.path.join(input_folder,exp_id,"{}a@p{}{}*".format(exp_id,s,year)))  
        # except OSError:
        #     continue
    for s in ["a","c","e"]:
        x=iris.load(os.path.join(input_folder,exp_id,"{}a@p{}{}*".format(exp_id,s,year)))  
        iris.save(x,os.path.join(output_folder,'{}_p{}{}.nc'.format(exp_id,s,Constants.um.from_um_filename_years(year))))

def main(input_folder=None,output_folder=None,exp_id=None,years=None):
    p=Pool(processes=ncpus)
    p.starmap(convert,zip(repeat(input_folder),repeat(exp_id),years,repeat(output_folder)))
    p.close()
    p.join()  
    
if __name__ == '__main__':
    main(input_folder,output_folder,exp_id,years)
    
