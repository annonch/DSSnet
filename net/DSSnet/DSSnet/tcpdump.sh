iperf3 -s >iperf.lg.txt 2>&1 &
tcpdump udp port 5201 -vv > tcpdump.log.txt  
