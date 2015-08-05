#!/bin/bash
#PBS -N w2vg
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=8
#PBS -l mem=8gb
#PBS -l scratch=16gb


log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
#i=1
#s=4
#w=5
#a=25
#m=3
#h=0
#n=0
#g=0

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
DATA_DIR="/storage/brno4-cerit-hsm/projects/sdata/hnizdja2_seznam/raw_texts"
# sg size window alpha*1000 mincount hs neg iter
MODEL_NAME=i$I-s$S-w$W-a$A-m$M-h$H-n$N-g$G
FILE_NAME="all"
TYPE=$NAME


cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying model file."
if [ -f $INPUT_DIR/models/$TYPE/$MODEL_NAME.word2vec ]
then
    cp $INPUT_DIR/models/$TYPE/$MODEL_NAME.* $SCRATCHDIR
    log_echo "Model found."
    else
    log_echo "Model not found."
   fi
log_echo "Copying data."
cp $DATA_DIR/$TYPE/$FILE_NAME.raw_text.gz $SCRATCHDIR
log_echo "Extracting data."
gunzip $SCRATCHDIR/$FILE_NAME.raw_text.gz
log_echo "Done."
log_echo "Running scripts..."
python $INPUT_DIR/w2vg.py $FILE_NAME $MODEL_NAME $G $S $W $A $M $H $N $I
log_echo "Done."
log_echo "Copying files..."
cp $SCRATCHDIR/$MODEL_NAME.* $INPUT_DIR/models/$TYPE
log_echo "Done."
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."