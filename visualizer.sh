#!/bin/bash
#PBS -N sparse
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=64gb
#PBS -l scratch=32gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

cd $SCRATCHDIR
N_JOBS=1

#cp $INPUT_DIR/bh_tsne/words.txt $SCRATCHDIR
#cp $INPUT_DIR/bh_tsne/bh_out/data_big.txt $SCRATCHDIR
cp $INPUT_DIR/visualizer.py $SCRATCHDIR
cp $INPUT_DIR/*.seg $SCRATCHDIR
python $SCRATCHDIR/visualizer.py

cp $SCRATCHDIR/*.txt $INPUT_DIR

log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."