#!/bin/bash
#PBS -N qvec
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=8gb
#PBS -l scratch=16gb

PATH_NAME="models/lemmatized/default"
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MODEL_NAME="content"
DATA_NAME="qid_text_unique.txt"
log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/$PATH_NAME/$MODEL_NAME.doc2vec ]
then
    cp $INPUT_DIR/$PATH_NAME/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
    exit 1
   fi
log_echo "Copying data."
cp $INPUT_DIR/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/qvec.py $SCRATCHDIR
python qvec.py
cp $SCRATCHDIR/*.pickle $INPUT_DIR
rm $SCRATCHDIR/*