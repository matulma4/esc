#!/bin/bash

gcc -o test.exe test.c
./test.exe 0
./bh_tsne
./test.exe 1 | less
