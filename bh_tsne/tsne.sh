#!/bin/bash

gcc -o test.exe test.c
./test.exe 0 $1 $2 data/$3
g++ sptree.cpp tsne.cpp -o bh_tsne -O2
./bh_tsne > $3_tsne_out.txt
./test.exe 1 > $3_out.txt
