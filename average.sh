#!/bin/bash
#PBS -N avg
#PBS -l walltime=48h
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
cp $INPUT_DIR/$PATH_NAME/$DOC_NAME $SCRATCHDIR
log_echo "Splitting the input file"
split -l 3920 -a 2 -d $DOC_NAME document_
mkdir $SCRATCHDIR/chunks
cp document_* $SCRATCHDIR/chunks
log_echo "Done."
cp $INPUT_DIR/thread_average.py $SCRATCHDIR
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
cp $INPUT_DIR/train.py $SCRATCHDIR
cp $INPUT_DIR/basicgrad.py $SCRATCHDIR
log_echo "Done."
python $SCRATCHDIR/thread_average.py 32 $MODEL_NAME.word2vec
log_echo "Done."
mkdir $INPUTDIR/chunks
mkdir $INPUTDIR/chunks/$DOC_NAME
cp $SCRATCHDIR/chunks/*.out $INPUT_DIR/chunks/$DOC_NAME
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."