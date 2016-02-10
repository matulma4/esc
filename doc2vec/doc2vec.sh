#!/bin/bash

#PBS -N doc2vec
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=8gb
#PBS -l scratch=16gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
FNAME="qtexts2.txt"
PTH="models/lemmatized/default"
MODEL="q_model"
cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying files..."
cp $INPUT_DIR/$FNAME $SCRATCHDIR
cp $INPUT_DIR/doc2vec.py $SCRATCHDIR
log_echo "Done"
log_echo "Running script..."
python $SCRATCHDIR/doc2vec.py $FNAME $MODEL
log_echo "Done"
log_echo "Copying result..."
cp $SCRATCHDIR/*.doc2vec* $INPUT_DIR
log_echo "Finished"