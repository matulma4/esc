#!/bin/bash
#PBS -N bm25
#PBS -l walltime=4h
#PBS -l nodes=1:ppn=1
#PBS -l mem=20gb
#PBS -l scratch=25gb

log_echo() {
  echo $(date "+%Y%m%d-%H.%M.%S") " $@";
}

module unload python34-modules-intel
module add python27-modules-gcc

cd $SCRATCHDIR
N_JOBS=1

python bm25.py

rm -rf $SCRATCHDIR/*