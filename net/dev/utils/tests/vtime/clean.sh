#!/bin/bash
echo 'cleaning'
{
rm /tmp/vtime_test.pipe
rm *~ 
rm *#
rm vtime.output
rm dilation.output
} &> /dev/null
echo ' '
exit
