#!/bin/bash

iter=50
for ftr in 773 774 775 776 777 778 779 780 781 782 783 925 ; do
for m in 0 1 2; do
qsub -v METRIC=$m,ITER=$iter,NUMBER=$ftr tester.sh
done
done