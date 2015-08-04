#!/bin/bash

#for nm in 'classic' 'lemmatized' ; do
#for iter in 1 2 3 4 5 ; do
#for size in 25 50 100 150 200 250 300 ; do
#for win in 1 2 3 5 10 ; do
iter=1
size=10
win=5
nm="lemmatized"
qsub -v I=$iter,S=$size,W=$win,A=25,M=5000,H=1,N=1,G=0,NAME=$nm w2v.sh
#done
#done
#done
#done