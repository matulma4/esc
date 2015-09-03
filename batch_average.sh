#!/bin/bash

split -l 125390 -a 2 -d $DOC_NAME document_
for a in document_* ; do
qsub -v $DOC_NAME=$a average.sh
done
rm document_*