#!/bin/bash

# keep the place tidy
#./clean.sh
echo 'testing Virtual time '
echo '3...'
sleep 1
echo ' 2...'
sleep 1
echo '  1...'
sleep 1


echo "Starting Program C"
# start program A
./C.py > vtime.output 2>&1 &

PID_PROGRAM_A=${!}
sleep 1
# Register A with Virtual Time
echo 'registering with virtual time'
echo 1000 > /proc/$PID_PROGRAM_A/dilation

DILATION=($(cat  /proc/$PID_PROGRAM_A/dilation))

sleep 1

if [ $DILATION = '1000' ]
then
    echo 'registration successful'
else
    echo 'registering process with virtual time failed'
fi

jobs

sleep 1

echo 'running for 20 seconds'
# run for 20 seconds
sleep 1
echo ' '
ps fj | head -n 6
echo ' '
sleep 18

echo 'freezing process A'
# pause A for 20 seconds
#kill -19 $PID_PROGRAM_A # use freeze interface instead 
echo 1 > /proc/$PID_PROGRAM_A/freeze
FREEZE=($(cat  /proc/$PID_PROGRAM_A/freeze))

sleep 1

if [ $FREEZE = '1' ]
then
    echo 'Freeze successful'
else
    echo 'Freeze failed'
fi

sleep 3
echo ' '
ps fj | head -n 6
echo ' '
sleep 17

# resume A and run for 20 more seconds
echo 'resume process A'
#kill -18 $PID_PROGRAM_A 
echo 0 > /proc/$PID_PROGRAM_A/freeze
FREEZE=($(cat  /proc/$PID_PROGRAM_A/freeze))
sleep 1
if [ $FREEZE = '0' ]
then
    echo 'unfreeze successful'
else
    echo 'unfreeze failed!'
fi

sleep 1
echo ' '
ps fj | head -n 6
echo ' '
sleep 1

echo 'running for 20 more seconds'
# wait for program B to finish (runs for 60 seconds)
wait $PID_PROGRAM_A

echo 'test finished'
cat vtime.output

