#!/bin/bash

#PBS -N ssi
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=64gb
#PBS -l scratch=16gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
mkdir $SCRATCHDIR/hashes
N_JOBS=1
log_echo "Copying files..."
cp $INPUT_DIR/qmodel2.doc2vec* $SCRATCHDIR
cp $INPUT_DIR/model.doc2vec* $SCRATCHDIR
cp $INPUT_DIR/doc_mapper.txt $SCRATCHDIR
cp $INPUT_DIR/hashes.txt $SCRATCHDIR
cp $INPUT_DIR/qids.txt $SCRATCHDIR
cp $INPUT_DIR/ssi_signal.py $SCRATCHDIR
log_echo "Done"
log_echo "Running script..."
python ssi_signal.py > ssi.signal.txt
log_echo "Done"
log_echo "Copying result..."
cp $SCRATCHDIR/ssi_signal.txt $INPUT_DIR
rm $SCRATCHDIR/*
log_echo "Finished"