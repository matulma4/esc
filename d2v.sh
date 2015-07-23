#!/bin/bash
#PBS -N d2vg
#PBS -l walltime=1h
#PBS -l nodes=1:ppn=1
#PBS -l mem=8gb
#PBS -l scratch=4gb


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
wget mattmahoney.net/dc/text8.zip
unzip text8.zip
python -m nltk.downloader punkt
python $INPUT_DIR/d2vg.py orig 0 0 0
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."