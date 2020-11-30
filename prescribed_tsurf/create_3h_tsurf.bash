#!/bin/bash

PROGNAME=$0

usage() {
  cat << EOF
Script to generate the 3h tsurf for tsurf prescription experiment.
Usage: $PROGNAME [-i <input folder>] [-o <output folder>]  ...

List of keys/options:
-i <path to folder> -> path to input folder
-o <path to file> -> path to output file
-s <string> -> stream (default is "c" for 3h sst).
-g -> add greb annual cycle tsurf response on top
--id <experiment id> -> experiment id (if not provided, the last directory of the input folder will be considered as id)
EOF
  exit 1
}

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
script="submission_script"
cat > "$script" <<EOF
#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -l ncpus=4
#PBS -q normal
#PBS -P w48
#PBS -l storage=gdata/hh5+gdata/w48+scratch/w48
#PBS -l mem=50gb

/g/data3/w48/dm5220/scripts/prescribed_tsurf/3h_tsurf.py${options}
EOF
qsub "$script"
