#!/bin/bash
#PBS -N bhtsne
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=4
#PBS -l mem=16gb
#PBS -l scratch=16gb

INPUT_DIR="/storage/brno2/home/$LOGNAME/esc/bh_tsne"

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
cd $SCRATCHDIR
N_JOBS=1
log_echo "Copying..."
cp $INPUT_DIR/* $SCRATCHDIR
rm $SCRATCHDIR/bh_tsne
rm $SCRATCHDIR/test.exe
cp $INPUT_DIR/../models/lemmatized/default/content.* $SCRATCHDIR
log_echo "Done"
log_echo "Starting..."
mkdir $SCRATCHDIR/data
python $SCRATCHDIR/bh.py content.word2vec
# /bin/bash tsne.sh $PERPLEXITY $THETA

# ./bh_tsne > tsne_out.txt
# ./test.exe > out.txt

#mkdir $INPUT_DIR/words/$MODEL-p$PERPLEXITY-t$THETA
#cp out.txt $INPUT_DIR/words/$MODEL-p$PERPLEXITY-t$THETA
#cp tsne_out.txt $INPUT_DIR/words/$MODEL-p$PERPLEXITY-t$THETA
#cp $SCRATCHDIR/data.dat $INPUT_DIR
cp $SCRATCHDIR/data/* $INPUT_DIR/data
log_echo "Done"
log_echo "Cleaning up..."
rm -rf $SCRATCHDIR/*
log_echo "Done."
log_echo "Finished."
