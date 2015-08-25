#!/bin/bash
#PBS -N extract
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=32gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
DATA_NAME="temp_features.rtData"
PATH_NAME="models/lemmatized/default"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1

cp $INPUT_DIR/$DATA_NAME $SCRATCHDIR
cp $INPUT_DIR/$PATH_NAME/content.raw_text $SCRATCHDIR
cp $INPUT_DIR/doc_mapper.txt.gz $SCRATCHDIR
gunzip $SCRATCHDIR/doc_mapper.txt.gz
cp $INPUT_DIR/extractor.py $SCRATCHDIR
cp $INPUT_DIR/doc_to_vec.py $SCRATCHDIR
cp $INPUT_DIR/appender.py $SCRATCHDIR
cp $INPUT_DIR/basicgrad.py $SCRATCHDIR
python $SCRATCHDIR/extractor.py
cp $SCRATCHDIR/temp_features.rtData $INPUT_DIR
rm -rf $SCRATCHDIR/*