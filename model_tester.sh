#!/bin/bash
#PBS -N model_tester
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=32gb
#PBS -l scratch=16gb

export LANG=cs_CZ
log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/matulma4/esc"
TYPE="classic"

cd $SCRATCHDIR
cp $INPUT_DIR/model_tester.py $SCRATCHDIR
N_JOBS=1
log_echo "Running scripts..."
for doc in $INPUT_DIR/models/$TYPE/*.word2vec ; do
cp $doc $SCRATCHDIR
cp $doc.* $SCRATCHDIR
python model_tester.py $doc
#cp $SCRATCHDIR/$doc.out $INPUT_DIR/models/$TYPE
done
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."