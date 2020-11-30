#!/bin/bash

PROGNAME=$0

usage() {
  cat << EOF
Script to generate the monthly sst for tsurf prescription experiment, and convert it to UM ancillary file format (via mkancil).
Usage: $PROGNAME [-i <input folder>] [-o <output folder>]  ...

List of keys/options:
-i <path to folder> -> path to input folder
-o <path to file> -> path to output UM ancillary file
-s <string> -> stream (default is "a" for monthly sst).
-g -> add greb annual cycle tsurf response on top
--id <experiment id> -> experiment id (if not provided, the last folder of the input path will be considered as id)
EOF
  exit 1
}
filetype="monthly_sst"
while getopts hi:o:s:-:g opt; do
    case $opt in
        -)
            case "$OPTARG" in
                id)
                    options+=" --id ${!OPTIND}"
		    id=${!OPTIND}
		    OPTIND=$(( $OPTIND + 1 ))
                    ;;
                *)
                echo "Uknown option --${OPTARG}"
                usage
            esac;;
        i)
            in=$(readlink -f "$OPTARG")
            options+=" -i $(readlink -f "$OPTARG")"
            ;;
        o)
            out=$(readlink -m "$OPTARG")
            ;;
        s)
            options+=" -s ${OPTARG}"
            ;;	    
        g)  options+=" -g"
            ;;	
        *) usage
    esac
done

if [[ -z $id ]]; then
    id=$(basename "$in")
    in="$(dirname $(dirname "$in"))/ancil/${id}_${filetype}.nc"
else
    in="$(dirname "$in")/ancil/${id}_${filetype}.nc"
fi
options+=" -o ${in}"
mkdir -p $(dirname "$in")
cd /g/data3/w48/dm5220/scripts/prescribed_tsurf

xancil_namelist="/g/data3/w48/dm5220/scripts/prescribed_tsurf/xancil.namelist_${filetype}"
cat > "$xancil_namelist" <<EOF
 &nam_config
  ICAL = 2,
  ISIZE = 64,
  L32BIT = .FALSE.,
  VERSION = 7.3,
  LBIGENDOUT = .TRUE.,
  LWFIO = .TRUE.,
  IWFIO_SIZE = 2048,
  NNCFILES = 1
  NCFILES = "${in}"
 /

 &nam_gridconfig
  LVARGRID = .FALSE.,
  IAVERT = 0,
  IOVERT = 0,
  LDEEPSOIL = .FALSE.
 /

 &nam_ozone
 /

 &nam_smow
 /

 &nam_slt
 /

 &nam_soil
 /

 &nam_veg
 /

 &nam_vegfrac
 /

 &nam_vegfunc
 /

 &nam_vegdist
 /
 
 &nam_sst
  LSST = .TRUE.,
  SST_FILEIN = "${in}"
  SST_NCNAME = "surface_temperature",
  SST_FILEOUT = "${out}"
  LSST_MIN = .TRUE.,
  ASST_MIN = 271.4,
  LSST_ICEVAL = .FALSE.,
  LSST_PERIODIC = .TRUE.,
  LSST_CAL_INDEP = .FALSE.,
  ISST_MASK =-1,
  ISST_TIMEUSAGE1 = 1,
  ISST_TIMEUSAGE2 = 0,
  ISST_STARTDATE(1) = 0000,
  ISST_STARTDATE(2) = 1,
  ISST_STARTDATE(3) = 16,
  ISST_STARTDATE(4) = 0,
  ISST_STARTDATE(5) = 0,
  ISST_STARTDATE(6) = 0,
  ISST_NTIMES = 12,
  ISST_INTERVAL = 1,
  ISST_INTUNIT = 1,
  LSST_MM = .TRUE.
 /
 
 &nam_ice
 /

 &nam_orog
 /

 &nam_mask
 /

 &nam_lfrac
 /

 &nam_ausrmulti
 /

 &nam_ausrancil
 /

 &nam_ts1
 /

 &nam_flux
 /

 &nam_ousrmulti
 /

 &nam_ousrancil
 /

 &nam_genanc_config
  NANCFILES = 1
 /

 &nam_genanc
  LGENANC_FILE(1) = .FALSE.,
 /

 &nam_astart
 /

EOF

script="submission_script_${filetype}"
cat > "$script" <<EOF
#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -l ncpus=4
#PBS -q normal
#PBS -P w48
#PBS -l storage=gdata/hh5+gdata/w48+scratch/w48+scratch/access
#PBS -l mem=50gb

echo "Writing Sea Surface Temperature netCDF file: ${in}"
/g/data3/w48/dm5220/scripts/prescribed_tsurf/${filetype}.py${options}
/scratch/access/apps/xancil/0.57/mkancil < "$xancil_namelist"
EOF

qsub "$script"
