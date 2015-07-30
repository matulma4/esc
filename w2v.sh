#!/bin/bash
#PBS -N w2vg
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
DATA_DIR="/storage/brno4-cerit-hsm/projects/sdata/hnizdja2_seznam/raw_texts/classic"
MODEL_NAME = "model"
FILE_NAME = "all"


cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/$MODEL_NAME.word2vec ]
then
    cp $INPUT_DIR/$MODEL_NAME.word2vec $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
   fi
log_echo "Copying data."
cp $DATA_DIR/$FILE_NAME.raw_text.gz $SCRATCHDIR
log_echo "Extracting data."
gunzip $SCRATCHDIR/$FILE_NAME.raw_text.gz
log_echo "Done."
log_echo "Running script..."
python $INPUT_DIR/w2vg.py $FILE_NAME $MODEL_NAME
log_echo "Done."
log_echo "Copying files..."
cp $SCRATCHDIR/$MODEL_NAME.word2vec $INPUT_DIR
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."