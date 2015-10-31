#!/bin/bash

#PBS -N feature_tester
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=8gb
#PBS -l scratch=16gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

echo $METRIC $ITER
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
FTR_NAME="new_text_features4.rtData"
cd $SCRATCHDIR
N_JOBS=1
cp $INPUT_DIR/data/* $SCRATCHDIR
cp $INPUT_DIR/$FTR_NAME $SCRATCHDIR
cp $INPUT_DIR/rank-py.py $SCRATCHDIR
cp $INPUT_DIR/feature_converter.py $SCRATCHDIR
python feature_converter.py $FTR_NAME $NUMBER_$FTR_NAME $NUMBER
python rank-py.py $METRIC $ITER
log_echo "Finished"
