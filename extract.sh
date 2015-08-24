#!/bin/bash
#PBS -N extract
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=32gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
DATA_NAME="base_text_features.rtData"
PATH_NAME="models/lemmatized/default"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1

cp $INPUT_DIR/$DATA_NAME
cp $INPUT_DIR/temp_mapper.txt
cp extractor.py $SCRATCHDIR
cp doc_to_vec.py $SCRATCHDIR
cp appender.py $SCRATCHDIR
python $SCRATCHDIR/extractor.py
cp $SCRATCHDIR/temp_features.rtData $INPUT_DIR
rm -rf $SCRATCHDIR/*