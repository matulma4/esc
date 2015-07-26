#!/bin/bash
#PBS -N d2vg
#PBS -l walltime=2h
#PBS -l nodes=1:ppn=1
#PBS -l mem=16gb
#PBS -l scratch=8gb


log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"

cd $SCRATCHDIR
N_JOBS=1

log_echo "Running script..."
# wget mattmahoney.net/dc/text8.zip
# unzip text8.zip
log_echo "Copying and running go.sh."
cp $INPUT_DIR/go.sh $SCRATCHDIR
/bin/bash go.sh
# cp -R $INPUT_DIR/aclImdb_v1.tar.gz $SCRATCHDIR
python -m nltk.downloader punkt
log_echo "Running orig."
python $INPUT_DIR/d2vg.py orig 0 0 0
cp orig.out $INPUT_DIR
log_echo "Running dm."
python $INPUT_DIR/d2vg.py dm 1 0 0
cp dm.out $INPUT_DIR
log_echo "Running hs."
python $INPUT_DIR/d2vg.py hs 0 1 0
cp hs.out $INPUT_DIR
log_echo "Running neg."
python $INPUT_DIR/d2vg.py neg 0 0 1
cp neg.out $INPUT_DIR
log_echo "Running max."
python $INPUT_DIR/d2vg.py max 0 1 1
cp max.out $INPUT_DIR
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."