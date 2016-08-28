#!/bin/bash

# keep the place tidy
#./clean.sh
echo 'testing Virtual time '
echo 'dilation test'
echo '3...'
sleep 1
echo ' 2...'
sleep 1
echo '  1...'
sleep 1

echo "Starting Program B"
# start program B
./B.py > dilation.output 2>&1 &
PID_PROGRAM_B=${!}

echo "Starting Program A"
# start program A
./A.py &
PID_PROGRAM_A=${!}
sleep 1
# Register A with Virtual Time
echo 'registering with virtual time'
echo 500 > /proc/$PID_PROGRAM_A/dilation

DILATION=($(cat  /proc/$PID_PROGRAM_A/dilation))

sleep 1

if [ $DILATION = '500' ]
then
    echo 'registration successful'
else
    echo 'registering process with virtual time failed'
fi

jobs

sleep 1

echo 'running for 60 seconds'
# run for 20 seconds
sleep 60
# wait for program B to finish (runs for 60 seconds)
wait $PID_PROGRAM_B
kill -s 9 $PID_PROGRAM_A

echo 'test finished'
echo 'check out the timestamps in test.output'

# kill if they got through somehow
{
pkill -9 A.py                                                                                                              
pkill -9 B.py
} &> /dev/null

sleep 3
cat dilation.output

