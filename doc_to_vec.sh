#!/bin/bash
#PBS -N doc2vec
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=16gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MODEL_NAME="model5"
DATA_NAME="temp_new.raw_text"
FTR_NAME="temp_features.rtData"
MAP_NAME="temp_mapper.txt"
AVG_NAME="dummy_averages.txt"
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
    exit 1
   fi
log_echo "Copying data."
cp $INPUT_DIR/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/$FTR_NAME $SCRATCHDIR
cp $INPUT_DIR/$MAP_NAME $SCRATCHDIR
cp $INPUT_DIR/$AVG_NAME $SCRATCHDIR
cp $INPUT_DIR/basicgrad.py $SCRATCHDIR
cp $INPUT_DIR/train.py $SCRATCHDIR
# gunzip $SCRATCHDIR/$MAP_NAME
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
log_echo "Done."
python $SCRATCHDIR/doc_to_vec.py
cp $SCRATCHDIR/doc_model.pickle $INPUT_DIR
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."