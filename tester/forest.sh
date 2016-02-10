#!/bin/bash
#PBS -N forest
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=8gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
MAP_NAME="doc_mapper.txt.gz"
AVG_NAME="R_old.mtx"
log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1
cp $INPUT_DIR/../hashes.txt $SCRATCHDIR
cp $INPUT_DIR/../relevances.txt $SCRATCHDIR
cp $INPUT_DIR/$MAP_NAME $SCRATCHDIR
gunzip $SCRATCHDIR/$MAP_NAME
cp $INPUT_DIR/$AVG_NAME $SCRATCHDIR
cp $INPUT_DIR/forest.py $SCRATCHDIR
python $SCRATCHDIR/forest.py
cp $SCRATCHDIR/*.pickle $INPUT_DIR
cp $SCRATCHDIR/score.txt $INPUT_DIR

log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."