#!/bin/bash

gcc -o test.exe test.c
./test.exe 0
./bh_tsne > tsne_out.txt
./test.exe 1 > out.txt
