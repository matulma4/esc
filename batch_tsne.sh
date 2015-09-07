#!/bin/bash

for a in {0..1} ; do
qsub -v PERPLEXITY=60,THETA=0.8,DATA_NAME=data$a.txt bh.sh
done