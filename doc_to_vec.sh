#!/bin/bash
#PBS -N doc2vec
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=16
#PBS -l mem=512gb
#PBS -l scratch=16gb

PATH_NAME="models/lemmatized/default"
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MODEL_NAME="model1"
DATA_NAME="content.raw_text"
FTR_NAME="base_text_features.rtData"
MAP_NAME="doc_mapper.txt.gz"
AVG_NAME="R_new.mtx"
log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/$MODEL_NAME.doc2vec ]
then
    cp $INPUT_DIR/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
    exit 1
   fi
log_echo "Copying data."
# cp $INPUT_DIR/$PATH_NAME/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/../$FTR_NAME $SCRATCHDIR
cp $INPUT_DIR/$MAP_NAME $SCRATCHDIR
cp $INPUT_DIR/$AVG_NAME $SCRATCHDIR
cp $INPUT_DIR/basicgrad.py $SCRATCHDIR
cp $INPUT_DIR/train.py $SCRATCHDIR
# cp $INPUT_DIR/newest_questions_content.pickle $SCRATCHDIR
gunzip $SCRATCHDIR/$MAP_NAME
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
split -l 41480 -a 2 -d $SCRATCHDIR/$FTR_NAME $SCRATCHDIR/feature_
log_echo "Done."
python $SCRATCHDIR/doc_to_vec.py
cp $SCRATCHDIR/*.pickle $INPUT_DIR
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."