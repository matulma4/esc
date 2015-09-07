#!/bin/bash

for a in {2..102} ; do
qsub -v PERPLEXITY=60,THETA=0.8,DATA_NAME=data$a.txt bh.sh
done