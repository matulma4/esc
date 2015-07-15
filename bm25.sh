#!/bin/bash
#PBS -N bm25
#PBS -l walltime=4h
#PBS -l nodes=1:ppn=4
#PBS -l mem=20gb
#PBS -l scratch=25gb


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
python -m nltk.downloader gutenberg
python $INPUT_DIR/bm25.py
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."