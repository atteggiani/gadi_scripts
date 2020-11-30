#!/bin/bash

PROGNAME=$0

usage() {
  cat << EOF
Script to generate the monthly sst for tsurf prescription experiment, and convert it to UM ancillary file format (via mkancil).
Usage: $PROGNAME [-i <input folder>] [-o <output folder>]  ...

List of keys/options:
-i <path to folder> -> path to input folder
-o <path to file> -> path to output UM ancillary file
-s <string> -> stream (default is "a" for monthly tsurf).
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
                    OPTIND=$(( $OPTIND + 1 ))
                    ;;
                *)
                echo "Uknown option --${OPTARG}"
                usage
            esac;;
        i)
	    options+=" -i $(readlink -f "$OPTARG")"
            ;;
        o)
            options+=" -o $(readlink -m "$OPTARG")"
            ;;
        s)
            options+=" -s ${OPTARG}"
            ;;
        g)  options+=" -g"
            ;;	
        *) usage
    esac
done

cd /g/data3/w48/dm5220/scripts/prescribed_tsurf

script="submission_script_${filetype}"
cat > "$script" <<EOF
#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -l ncpus=48
#PBS -q normal
#PBS -P w48
#PBS -l storage=gdata/hh5+gdata/w48+scratch/w48
#PBS -l mem=50gb

/g/data3/w48/dm5220/scripts/prescribed_tsurf/${filetype}.py${options}
EOF

qsub "$script"
