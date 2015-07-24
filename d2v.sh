#!/bin/bash
#PBS -N d2vg
#PBS -l walltime=2h
#PBS -l nodes=1:ppn=1
#PBS -l mem=16gb
#PBS -l scratch=8gb


log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"

cd $SCRATCHDIR
N_JOBS=1

log_echo "Running script..."
# wget mattmahoney.net/dc/text8.zip
# unzip text8.zip
/bin/bash go.sh
python -m nltk.downloader punkt

python $INPUT_DIR/d2vg.py orig 0 0 0
python $INPUT_DIR/d2vg.py dm 1 0 0
python $INPUT_DIR/d2vg.py hs 0 1 0
python $INPUT_DIR/d2vg.py neg 0 0 1
python $INPUT_DIR/d2vg.py max 0 1 1
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."