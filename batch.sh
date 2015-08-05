#!/bin/bash

for nm in 'classic' 'lemmatized' ; do
#for iter in 1 2 3 4 5 ; do
# for size in 50 100 200 300 ; do
# for win in 3 5 10 ; do
for fn in 'content' 'header' 'title' 'url' ; do
# iter=1
# size=10
# win=5
# nm="lemmatized"
qsub -v I=1,S=100,W=5,A=25,M=5,H=1,N=0,G=1,NAME=$nm,FILE_NAME=$fn w2v.sh
done
done
#done
# done
# done