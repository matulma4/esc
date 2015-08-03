#!/bin/bash

for min in 5 10 50 ; do
for sg in 0 1 ; do
qsub -v I=1,S=4,W=5,A=25,M=$min,H=1,N=1,G=$sg w2v.sh
done
done