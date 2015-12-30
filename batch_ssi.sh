#!/bin/bash

for i in 10000 100000 1000000 ; do
for a in 0.1 0.01 0.001 0.0001 ; do
qsub -v ALPHA=$a,N_ITER=$i ssi.sh
done
done