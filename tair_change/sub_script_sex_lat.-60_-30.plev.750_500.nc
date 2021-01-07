#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -l ncpus=1
#PBS -q normal
#PBS -P w48
#PBS -l storage=gdata/hh5+gdata/w48+scratch/w48+gdata/access
#PBS -l mem=50gb

/g/data/access/projects/access/apps/xancil/0.57/mkancil < "/g/data3/w48/dm5220/scripts/tair_change/xancil.namelist_sex_lat.-60_-30.plev.750_500.nc"
/g/data/w48/dm5220/scripts/util/fix_polar_anom "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/sensitivity_exp/lat.-60_-30.plev.750_500" #fix polar errors
ln -s "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/sensitivity_exp/lat.-60_-30.plev.750_500" "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/sensitivity_exp/sex26"
