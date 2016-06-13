#!/bin/bash
sudo rm ./tmp/*
sudo touch ./tmp/pidlist
sudo rm /tmp/fifo.tmp
sudo rm *~
sudo rm *.pyc
sudo pkill freeze_listen
sudo mn -c
