#!/bin/bash
#PBS -N w2vg
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
DATA_DIR="/storage/brno4-cerit-hsm/projects/sdata/hnizdja2_seznam/raw_texts/classic"

cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/model.word2vec ]
then
    cp $INPUT_DIR/model.word2vec $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
   fi
log_echo "Copying data."
cp $DATA_DIR/all.raw_text.gz
log_echo "Extracting data."
gunzip $SCRATCHDIR/all.raw_text.gz
log_echo "Done."
log_echo "Running script..."
python $INPUT_DIR/w2vg.py
log_echo "Done."
log_echo "Copying files..."
cp $SCRATCHDIR/model.word2vec $INPUT_DIR
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."