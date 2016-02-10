#!/bin/bash
#PBS -N job_name
#PBS -l walltime=4h
#PBS -l nodes=1:ppn=1
#PBS -l mem=20gb
#PBS -l scratch=25gb

#Good to use for debugging
log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

# switch to the Python 2/3 environment
# -> you can use the profile file with some configurations

# usage: source /storage/brno2/home/$LOGNAME/.profile_python2

# EXAMPLE of the .profile file:
# ===================================================================================================================
# export PATH=/storage/brno2/home/hnizdja2/diplomathesis/lib/protobuf/bin:/usr/lib/cuda:$PATH
# export LD_LIBRARY_PATH=/storage/brno2/home/hnizdja2/diplomathesis/lib/protobuf/lib:$LD_LIBRARY_PATH

## reset variables
# PYTHONPATH=""

## this is for using python version 3.4, you can use similarly for python 2.x - IMPORTANT
# module unload python27-modules-intel
# module add python34-modules-gcc

## Python variables - IMPORTANT
# export PYTHONUSERBASE=/storage/brno2/home/hnizdja2/.local
# export PATH=$PYTHONUSERBASE/bin:$PATH
# export PYTHONPATH=$PYTHONUSERBASE/lib/python3.4/site-packages:$PYTHONPATH

## Protocol buffers python implementation
# export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
# export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=2

# source /storage/brno2/home/hnizdja2/.bashrc
#===================================================================================================================


cd $SCRATCHDIR

#number of processors
N_JOBS=1

# ---------------------------------------------------------------------------------
# START Prepare variables for the script
# ---------------------------------------------------------------------------------

INPUT_DIR="/storage/brno2/home/$LOGNAME/diplomathesis"

INPUT_FILE=/storage/brno2/home/hnizdja2/diplomathesis/input/$DATA_PATH

DICTIONARY_PATH=$INPUT_DIR/input/dicts/
MODEL_PATH=$INPUT_DIR/input/corpuses/

# ---------------------------------------------------------------------------------
# END
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# START Copy appropriate files for your job
# ---------------------------------------------------------------------------------

cd $SCRATCHDIR

log_echo "Copy BASE dataset"
cp $DICTIONARY_PATH/$DICT_NAME $SCRATCHDIR/dictionary.pruned
cp $MODEL_PATH/$MODEL_NAME $SCRATCHDIR/model
cp $INPUT_FILE $SCRATCHDIR/${DATA_NAME}.gz
gunzip $SCRATCHDIR/*.gz
log_echo "Done."

# ---------------------------------------------------------------------------------
# END
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# START Run appropriate python script with CLI
# ---------------------------------------------------------------------------------

log_echo "Creating extended queries..."
python $INPUT_DIR/create_features/run_simhash.py -d dictionary.pruned -m model -$TYPE $DATA_NAME -o ${OUTPUT_NAME}.mm
log_echo "Done."

# ---------------------------------------------------------------------------------
# END
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# START Copy results to my directory and clean the computation node
# ---------------------------------------------------------------------------------

log_echo "Copying results..."
gzip ${OUTPUT_NAME}.mm
cp ${OUTPUT_NAME}.mm* $INPUT_DIR/input/simhash/

log_echo "Done."

rm -rf $SCRATCHDIR/*

# ---------------------------------------------------------------------------------
# END
# ---------------------------------------------------------------------------------