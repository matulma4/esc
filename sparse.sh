#!/bin/bash
#PBS -N sparse
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=32
#PBS -l mem=64gb
#PBS -l scratch=32gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MODEL_NAME="content"
DATA_NAME="content.raw_text"
PATH_NAME="models/lemmatized/default"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/$PATH_NAME/$MODEL_NAME.word2vec ]
then
    cp $INPUT_DIR/$PATH_NAME/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
    exit 1
   fi
log_echo "Copying data."
cp $INPUT_DIR/$PATH_NAME/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/*.dic $SCRATCHDIR
cp $INPUT_DIR/*.mtx $SCRATCHDIR
cp $INPUT_DIR/dict_big.txt $SCRATCHDIR
log_echo "Done."
cp $INPUT_DIR/thread_average.py $SCRATCHDIR
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
cp $INPUT_DIR/train.py $SCRATCHDIR
cp $INPUT_DIR/basicgrad.py $SCRATCHDIR
log_echo "Done."
python $SCRATCHDIR/thread_average.py $DATA_NAME $MODEL_NAME.word2vec
log_echo "Done."
cp $SCRATCHDIR/*.mtx $INPUT_DIR
cp $SCRATCHDIR/*.dic $INPUT_DIR
# cp $SCRATCHDIR/*.txt $INPUT_DIR
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."