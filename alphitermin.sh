#!/bin/bash
#PBS -N w2vg
#PBS -l walltime=24h
#PBS -l nodes=2:ppn=4
#PBS -l mem=8gb
#PBS -l scratch=16gb


log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
DATA_DIR="/storage/brno4-cerit-hsm/projects/sdata/hnizdja2_seznam/raw_texts/classic"
# sg size window alpha*1000 mincount hs neg iter

FILE_NAME="all"


cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/$MODEL_NAME.word2vec ]
then
    cp $INPUT_DIR/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
   fi
log_echo "Copying data."
cp $DATA_DIR/$FILE_NAME.raw_text.gz $SCRATCHDIR
log_echo "Extracting data."
gunzip $SCRATCHDIR/$FILE_NAME.raw_text.gz
log_echo "Done."
log_echo "Running scripts..."
for i in 0.025 0.05 0.1 0.5 1
do
for j in 1 50 100 500 1000
do
for k in 5 10 15
do
MODEL_NAME=i1_s4_w5_a25_m3_h$j_n$k_g$i
python $INPUT_DIR/w2vg.py $FILE_NAME $MODEL_NAME $i 4 5 25 3 $j $k 1
done
done
done
log_echo "Done."
log_echo "Copying files..."
cp $SCRATCHDIR/$MODEL_NAME.* $INPUT_DIR
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."
