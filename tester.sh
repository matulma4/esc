#!/bin/bash

#PBS -N feature_tester
#PBS -l walltime=24h
#PBS -l nodes=1:ppn=1
#PBS -l mem=8gb
#PBS -l scratch=16gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

echo $METRIC $ITER
log_echo "Starting..."
source /storage/brno2/home/$LOGNAME/.profile_matulma4
log_echo "Done."
INPUT_DIR="/storage/brno2/home/$LOGNAME/esc"
FTR_NAME="new_text_features4.rtData"
cd $SCRATCHDIR
N_JOBS=1
mkdir $SCRATCHDIR/data
cp $INPUT_DIR/$FTR_NAME $SCRATCHDIR
cp $INPUT_DIR/rank-py.py $SCRATCHDIR
cp $INPUT_DIR/feature_converter.py $SCRATCHDIR
python $SCRATCHDIR/feature_converter.py $FTR_NAME $SCRATCHDIR/$NUMBER-$FTR_NAME $NUMBER
split -l 442239 -a 2 -d $NUMBER-$FTR_NAME document_
# ls $SCRATCHDIR
mv $SCRATCHDIR/document_00 $SCRATCHDIR/data/train.txt
mv $SCRATCHDIR/document_01 $SCRATCHDIR/data/test.txt
mv $SCRATCHDIR/document_02 $SCRATCHDIR/data/vali.txt
python $SCRATCHDIR/rank-py.py $METRIC $ITER
log_echo "Finished"
