#!/bin/bash
#PBS -N avg
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=16
#PBS -l mem=32gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MODEL_NAME="model5"
DATA_NAME="temp.raw_text"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/$MODEL_NAME.word2vec ]
then
    cp $INPUT_DIR/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
   fi
log_echo "Copying data."
# cp $INPUT_DIR/models/lemmatized/default/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/thread_average.py $SCRATCHDIR
log_echo "Done."
python $SCRATCHDIR/thread_average.py
log_echo "Done."
cp $SCRATCHDIR/averages.txt $INPUT_DIR
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."