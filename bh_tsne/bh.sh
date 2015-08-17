#!/bin/bash
#PBS -N bhtsne
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=16gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc/bh_tsne"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying..."
cp $INPUT_DIR/* $SCRATCHDIR
log_echo "Done"
log_echo "Starting..."
python $SCRATCHDIR bh.py
/bin/bash tsne.sh
cp out.txt $INPUT_DIR
cp tsne_out.txt $INPUT_DIR
log_echo "Done"
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."