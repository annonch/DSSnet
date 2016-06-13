#!/usr/bin/env bash

#download kernel

mkdir ~/virtual
cd ~/virtual

#dependencies
sudo apt-get install -y unzip

#get files

wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.16.3.tar.gz

tar zxfv linux-3.16.3.tar.gz
#download git

rm *.gz

#wget https://github.com/littlepretty/VirtualTimeKernel/archive/master.zip
#wget https://github.com/littlepretty/VirtualTimeKernel/archive/master.zip
#unzip master.zip
#rm *.zip

git clone https://github.com/littlepretty/VirtualTimeKernel.git

chmod +x ~/virtual/VirtualTimeKernel/transfer.sh
chmod +x ~/virtual/VirtualTimeKernel/build_all.sh

cd ~/virtual/VirtualTimeKernel/
sudo ~/virtual/VirtualTimeKernel/transfer.sh ~/virtual/linux-3.16.3
cd ~/virtual/linux-3.16.3/
sudo ~/virtual/linux-3.16.3/build_all.sh

