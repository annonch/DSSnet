#!/bin/bash

SCALE="1 10 50 100 250 500"
for scale in $SCALE
do
        # python benchmark_pause.py $scale > ${scale}.log
        perl parser.pl ${scale}.log.file freeze_${scale}.txt unfreeze_${scale}.txt
done

python cdfPlotAll.py # output figure will be ScaleFrzCDF.eps
python avgPlotAll.py # output figure will be ScaleFrzAvg.eps


