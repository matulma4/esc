#!/bin/bash

for model in "lemmatized" "classic" ; do
for theta in 0.2 0.4 0.6 0.8 1 ; do
for perplexity in 60 80 100 ; do
qsub -v MODEL=$model,THETA=$theta,PERPLEXITY=$perplexity bh.sh
done
done
done
