#!usr/bin/sh




#1 host
#10 hosts
#50 hosts
#100 hosts
#250 hosts
#1000 hosts
#'''



sleep 1

sudo python benchmark_pause.py 1 1.log
sleep 1
sudo mn -c
sleep 1

sudo python benchmark_pause.py 10 10.log
sleep 1
sudo mn -c
sleep 1

sudo python benchmark_pause.py 50 50.log
sleep 1
sudo mn -c
sleep 1

sudo python benchmark_pause.py 100 100.log
sleep 1
sudo mn -c
sleep 1

sudo python benchmark_pause.py 250 250.log
sleep 1
sudo mn -c
sleep 1

sudo python benchmark_pause.py 1000 1000.log
sleep 1
sudo mn -c
sleep 1
