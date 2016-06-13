#!/bin/bash

echo "hello and welcome to the fanciest grapher you wish was way easier to use"
echo "created by yours truly: Albert Einstein"
echo " not really...."
echo " use: pathToVTpingOutPut bl x_min x_max y_min y_max"

perl pingParse.pl $1 > /tmp/vt.cdf
perl pingParse.pl $2 > /tmp/bl.cdf

python cdfPlot.py /tmp/vt.cdf /tmp/bl.cdf $3 $4 $5 $6




