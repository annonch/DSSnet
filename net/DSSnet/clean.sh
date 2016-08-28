#!/bin/bash
sudo pkill java
sudo pkill python
sudo killall -s SIGKILL /usr/bin/java
sudo rm ./tmp/*
sudo touch ./tmp/pidlist
sudo rm /tmp/fifo.tmp
sudo rm *~
sudo rm *.pyc
sudo rm ./models/*.pyc
sudo pkill freeze_listen
sudo mn -c
sudo fuser -k 6653/tcp
sudo rm *.log
sudo rm ./logs/*.log
echo ' good to go! '
exit 
