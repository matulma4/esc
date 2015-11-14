#!/bin/bash
#PBS -N ordinal
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=128gb
#PBS -l scratch=16gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
FNAME="rel4.txt"
MODEL="model2.doc2vec"
cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying files..."
cp $INPUT_DIR/$FNAME $SCRATCHDIR
cp $INPUT_DIR/$MODEL $SCRATCHDIR
cp $INPUT_DIR/ord_regression.py $SCRATCHDIR
cp $INPUT_DIR/logistic.py $SCRATCHDIR
log_echo "Done"
log_echo "Running script..."
python $SCRATCHDIR/ord_regression.py $MODEL $FNAME
log_echo "Done"
log_echo "Copying result..."
cp $SCRATCHDIR/*.pickle $INPUT_DIR
log_echo "Finished"