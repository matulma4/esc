#!/bin/bash

#PBS -N ssi
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=64gb
#PBS -l scratch=16gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
FNAME="qtexts2.txt"
PTH="models/lemmatized/default"
MODEL="q_model2"
cd $SCRATCHDIR
mkdir $SCRATCHDIR/questions
mkdir $SCRATCHDIR/hashes
N_JOBS=1
log_echo "Copying files..."
cp $INPUT_DIR/$MODEL.doc2vec* $SCRATCHDIR
cp $INPUT_DIR/model2.doc2vec* $SCRATCHDIR
cp $INPUT_DIR/supervised_indexing.py $SCRATCHDIR
cp $INPUT_DIR/qa_tuple.py $SCRATCHDIR
cp $INPUT_DIR/qid_unique.txt $SCRATCHDIR
cp $INPUT_DIR/hashes2.txt $SCRATCHDIR
cp $INPUT_DIR/doc_mapper.txt $SCRATCHDIR
for f in $INPUT_DIR/ftr_dir/scratch/matulma4/job_10028766.arien.ics.muni.cz/*.txt ; do
cp $f $SCRATCHDIR/questions;
done
for g in $INPUT_DIR/ftr_dir/hashes/scratch/matulma4/job_10127101.arien.ics.muni.cz/*.txt ; do
cp $g $SCRATCHDIR/hashes;
done
log_echo "Done"
log_echo "Running script..."
python supervised_indexing.py qid_unique.txt q_model2.doc2vec model2.doc2vec 1000000 0.0001
log_echo "Done"
log_echo "Copying result..."
cp $SCRATCHDIR/*.pickle $INPUT_DIR
log_echo "Finished"