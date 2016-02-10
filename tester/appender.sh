#!/bin/bash
#PBS -N append
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
FTR_NAME="base_text_features.rtData"
cd $SCRATCHDIR
N_JOBS=1
cp $INPUT_DIR/../$FTR_NAME $SCRATCHDIR
cp $INPUT_DIR/basicgrad.py $SCRATCHDIR
cp $INPUT_DIR/train.py $SCRATCHDIR
cp $INPUT_DIR/signals.pickle $SCRATCHDIR
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
cp $INPUT_DIR/appender.py $SCRATCHDIR
python $SCRATCHDIR/appender.py

cp $SCRATCHDIR/new_text_features.rtData $INPUT_DIR
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."