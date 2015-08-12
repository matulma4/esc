#!/bin/bash
#PBS -N doc2vec
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=16gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MODEL_NAME="content"
DATA_NAME="content.raw_text"
FTR_NAME="base_text_features.rtData"
MAP_NAME="doc_mapper.txt.gz"
log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/models/lemmatized/default/$MODEL_NAME.word2vec ]
then
    cp $INPUT_DIR/models/lemmatized/default/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
   fi
log_echo "Copying data."
# cp $INPUT_DIR/models/lemmatized/default/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/$FTR_NAME $SCRATCHDIR
cp $INPUT_DIR/$MAP_NAME $SCRATCHDIR
gunzip $SCRATCHDIR/$MAP_NAME
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
log_echo "Done."
python $SCRATCHDIR/doc_to_vec.py
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."