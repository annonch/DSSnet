#!/usr/bin/env bash

# install packages
sudo apt-get update

sudo apt-get install -y htop
sudo apt-get install -y python3-pip
sudo apt-get install -y python-matplotlib
sudo apt-get install -y python3-matplotlib

#dependencies
sudo pip install pyzmq
sudo pip3 install pyzmq

mkdir ~/cosim
cd ~/cosim

# get the files

#git clone https://github.com/channon1/DSSnet



##########  Benchmarking    ########


# dependency for ping
# git clone https://github.com/iputils/iputils.git iputils
sudo apt-get install -y libcap-dev libssl-dev libidn11-dev openssl nginx
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y gnutls-bin libgnutls-dev
#compile
sudo make

# cd ~/cosim/DSSnet/benchmark/iperf
# git clone https://github.com/esnet/iperf.git iperf

#cd iperf
#sudo ./configure
#sudo make
#sudo make install

