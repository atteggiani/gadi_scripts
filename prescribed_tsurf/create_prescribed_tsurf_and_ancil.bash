#!/bin/bash

module use ~access/modules
module load pythonlib/umfile_utils

PROGNAME=$0

usage() {
  cat << EOF
Script to generate the 3h tsurf and monthly sst for tsurf prescription experiment and convert them to UM ancillary file format (via mkancil).
For the options, give first 3h and then monthly input separated by space (e.g. -i "input3h inputmonthly").
Usage: $PROGNAME [-i <input folder>] [-o "<output file 3h tsurf> <output file monthly sst>"]  ...

List of keys/options:
-i "<path to 3h folder> <path to monthly folder>" -> paths to input folders (if only one path provided, it will be used for both 3h and monthly data)
-o "<path to 3h file> <path to monthly file>" -> paths to output UM ancillary files
-s "<string1> <sting2>" -> streams (default is "c" for 3h tsurf and "a" for monthly sst).
-g -> add greb annual cycle tsurf response on top
EOF
  exit 1
}

filetype=("3h_tsurf" "monthly_sst")
for i in "${!filetype[@]}"
do
    OPTIND=1
    while getopts hi:o:s:g opt; do
        case $opt in
            i)
                arg=(${OPTARG})
                if [[ ${#arg[@]} == 2 ]]; then
                    in=$(readlink -f arg[$i])
                else
                    in=$(readlink -f "$OPTARG")
                fi		    
                options+=" -i $in"
                ;;
            o)
                arg=(${OPTARG})
		        out=$(readlink -m arg[$i])
                ;;
            s)
                arg=(${OPTARG})
                options+=" -s ${arg[$i]}"
                ;;
	    g)  options+=" -g"
		g=true
		;;    
            *) usage
        esac
    done

    if [[ -z $id ]]; then
        id=$(basename "$in")
        in="$(dirname $(dirname "$in"))/ancil/${id}${g+.greb}_${filetype[$i]}.nc"
    else
        in="$(dirname "$in")/ancil/${id}${g+.greb}_${filetype[$i]}.nc"
    fi
    options+=" -o ${in}"
    mkdir -p $(dirname "$in")

    cd /g/data3/w40/dm5220/scripts/prescribed_tsurf

    xancil_namelist="/g/data3/w40/dm5220/scripts/prescribed_tsurf/xancil.namelist_$(basename "$in")"
    namelist="$xancil_namelist"
    num=0
    while [[ -e "$namelist" ]]; do
    	num=$(( num + 1 ))
	namelist="${xancil_namelist}_${num}"
    done
    xancil_namelist="$namelist"


    if [[ $i == 0 ]]; then
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
  IAVERT = 1,
  NLEV = 38,
  NO3LEV = 38,
  LLEVSTOREUP = .TRUE.,
  NAM_VERT = "/g/data/access/projects/access/umdir/vn7.3/ctldata/vert/vertlevs_G3",
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
  LAUSRMULTI = .TRUE.,
  AUSRMULTI_FILEOUT = "${out}",
  LAUSRMULTI_PERIODIC = .TRUE.,
  LAUSRMULTI_CAL_INDEP = .FALSE.,
  IAUSRMULTI_TIMEUSAGE1 = 1,
  IAUSRMULTI_TIMEUSAGE2 = 0,
  IAUSRMULTI_STARTDATE(1) = 0000,
  IAUSRMULTI_STARTDATE(2) = 1,
  IAUSRMULTI_STARTDATE(3) = 1,
  IAUSRMULTI_STARTDATE(4) = 3,
  IAUSRMULTI_STARTDATE(5) = 0,
  IAUSRMULTI_STARTDATE(6) = 0,
  IAUSRMULTI_NTIMES = 2880,
  IAUSRMULTI_INTERVAL = 3,
  IAUSRMULTI_INTUNIT = 3,
  LAUSRMULTI_MM = .TRUE.
  IAUSRMULTI_NFIELD = 1
  IAUSRMULTI_FILEINID(1) = 1,
  IAUSRMULTI_STASHCODE(1) = 321,
  IAUSRMULTI_PPCODE(1) = 0,
  AUSRMULTI_NCNAME(1) = "surface_temperature",
  LAUSRMULTI_THETA(1) = .FALSE.
  IAUSRMULTI_GRIDTYPE(1) = 1,
  IAUSRMULTI_DATATYPE(1) = 1,
  IAUSRMULTI_MASKTYPE(1) = 2,
  IAUSRMULTI_MASK(1) = 0,
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
    else
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
    fi
    script="submission_script_${filetype[$i]}"
    cat > "$script" <<EOF
#!/bin/bash
#PBS -l walltime=00:10:00
#PBS -l ncpus=4
#PBS -q normal
#PBS -P w40
#PBS -l storage=gdata/hh5+gdata/w40+scratch/w40+gdata/access
#PBS -l mem=50gb

echo "Writing Surface Temperature netCDF file: ${in}"
python3 /g/data3/w40/dm5220/scripts/prescribed_tsurf/${filetype[$i]}.py${options}
/g/data/access/projects/access/apps/xancil/0.57/mkancil < "$xancil_namelist"
/g/data/w40/dm5220/scripts/util/fix_polar_anom.py "$out" #fix polar errors
EOF
    
    qsub "$script"
done
