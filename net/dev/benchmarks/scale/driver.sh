#!/bin/bash

read -d '' AwkScript << 'EOF'
BEGIN {
}
{ 
        if ($1 == "freeze") {
                print $2 >> "freeze.log"
        } else if ($1 == "unfreeze") {
                print $2 >> "unfreeze.log"
        }
}
END{
}
EOF

SCALE="10"
for scale in $SCALE
do
        > freeze.log
        > unfreeze.log
        python benchmark_pause.py $scale > ${scale}.log

        awk "$AwkScript" ${scale}.log
        python cdfPlot.py freeze.log unfreeze.log Scale${scale}FrzOvhd.eps
done

