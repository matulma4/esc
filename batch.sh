#!/bin/bash

for min in 5 10 50 ; do
for sg in 0 1 ; do
qsub -v i=1,s=4,w=5,a=25,m=$min,h=1,n=1,g=$sg w2v.sh
done
done