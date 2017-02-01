# DSSnet #

### Requirements for installation: ###
* Ubuntu / Debian ... Should work on windows and osx.. (not tested yet)
* Vagrant
* Virtual-box 
* Windows (VM) 

###  Use  ###
* DSSnet combines a power grid simulator (OpenDSS) with a SDN emulator (mininet). The software is designed to get high fidelity results of smart grid networks that require both communication and power. 
* Version 3.0

## How do I get set up? ##

### Navigate to /net/ ###

#### Set up the network emulation ####
* get this repository
* navigate to /net/LINUX-VM/
* run vagrant up
* may take a while to download image
* Seriously it may take quite a while
* If the message 
 ```
 default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Connection timeout. Retrying...
    default: Warning: Authentication failure. Retrying...
    default: Warning: Authentication failure. Retrying...
    default: Warning: Authentication failure. Retrying...
    default: Warning: Authentication failure. Retrying...
```
* this is some problem because of the re-packaging from an existing box just WAIT and ignore until it times out
* run vagrant ssh to log in. If it prompts for password use `vagrant`
* see vagrant docs for more info on vagrant (other useful commands vagrant destroy and vagrant halt)
* IMPORTANT: If the box does not load after timing out run `vagrant destroy` then `vagrant up` and let it time out with the above error message.

#### Setup Windows ####
* Get windows VM (win 7 onwards)
* Get python + numpy, win32com, (andaconda is easy for this stuff) [ tutorial to come ] 
* text editor
* IMPORTANT: create the following directory, C:\DSS and put the repository here
* IMPORTANT: the full path to the power coordinator should be C:\\DSS\DSSnet\dss\powerCoord2.py

#### Setup Network  ####
* open port on windows, default 50021
* make sure to test that the linux vm can communicate with the windows vm (try telnet)

### Windows TEST ###
#### test ####
* on windows navigate to dss folder in repository
* run `python powerCoord.py --trace 1 -et 1`
* What this is doing is sending in a trace file of events like the network coordinator would do to make sure that everything is good on the windows side.
* Note the IED files and the load/generation files should be in this directory along side the powerCoord.py ( I will try to make this easier soon )
* the configuration file defaults to the test case in the folder test 
* the trace file defaults to the test folder synch.trace
* the export monitors are in the folder that the circuit configuration file is in
* type `python powerCoord.py -h` to see all the options
```
usage: powerCoord.py [-h] [-trace TRACE] [-trace_file TRACE_FILE] [--version]
                     [-ip IP] [-port PORT] [-IED IED_CONFIG]
                     [-cf CIRCUIT_FILENAME] [-ts TIMESTEP] [-et ET]
                     [-mode MODE] [-mode_number MODE_NUMBER]

Manages power system simulation and synchronizes with the network coordinator

optional arguments:
  -h, --help            show this help message and exit
  -trace TRACE          "-trace 1" for yes: instead of using network emulator
                        we can use a trace of synchronization events from file
  -trace_file TRACE_FILE
                        location for trace file
  --version             show program's version number and exit
  -ip IP                ip of power coordinator
  -port PORT            port reserved for power coordinator
  -IED IED_CONFIG, --IED_config IED_CONFIG
                        path to IED file
  -cf CIRCUIT_FILENAME, --circuit_filename CIRCUIT_FILENAME
                        path to main circuit file
  -ts TIMESTEP, --timestep TIMESTEP
                        resolution of time step
  -et ET                time the experiment should end
  -mode MODE            mode the simulator should be ran in: "Snap", "Duty",
                        "Harmonics", "Direct","Dynamics": default is duty
  -mode_number MODE_NUMBER, -mn MODE_NUMBER
                        number of solutions done in different modes. Warning
                        this advances the clock (I believe that you can just
                        set the timestep to a good value and be okay)
```
### Linux TEST ###
#### test ####
* navigate to  C:\DSS\DSSnet\dss on windows
* run `python powerCoord.py -ip x.x.x.x whatever the ip of your win vm is
* navigate to  ~/DSSnet/net/DSSnet/ on linux
* run `sudo python netCoord.py -ip x.x.x.x whatever the ip of your win vm is
* You should see 

```
 sudo ./netCoord.py 
kernel switch used
custom controller
ovs in virtual time
Opening Connection to tcp://10.47.142.26:50021
/usr/local/var/run/openvswitch/ovsdb-server.pid
dilate_all_procs -t 0 -p 1184 1182 
no pipe info given
no pipe info given
no pipe info given
no pipe info given
no pipe info given
no pipe info given
*** Creating network
*** Adding controller
*** Adding hosts:
estest f1 gtest1 ltest1 mtest1 mtest2 
*** Adding switches:
s1 s2 s3 s4 s5 s6 
*** Adding links:
(s1, ltest1) (s1, s2) (s2, gtest1) (s2, s3) (s3, estest) (s3, s4) (s4, mtest1) (s4, s5) (s5, f1) (s5, mtest2) (s5, s6) 
*** Configuring hosts
estest f1 gtest1 ltest1 mtest1 mtest2 
*** Starting controller
c0 
*** Starting 6 switches
s1 s2 s3 s4 s5 s6 ...
Dumping Host Connections
estest estest-eth0:s3-eth3
f1 f1-eth0:s5-eth4
gtest1 gtest1-eth0:s2-eth3
ltest1 ltest1-eth0:s1-eth2
mtest1 mtest1-eth0:s4-eth3
mtest2 mtest2-eth0:s5-eth3
pids in virtual time:   1182 1184 1182 1184 19783 19785 19787 19789 19791 19793 19798 19801 19804 19807 19810 19813 19776
initiation finished
*** Starting CLI:
```

* At this point type `start`

```
DSSnet -->  start
sudo python ./models/test/load.py ltest1 &

sudo python ./models/test/gen.py gtest1 &

sudo python ./models/test/es.py estest &

sudo python ./models/test/mon0.py mtest1 &

sudo python ./models/test/mon1.py mtest2 &

sudo python ./models/test/fault.py f1 &

creating pipe: ./tmp/ltest1 
creating pipe: ./tmp/gtest1 
creating pipe: ./tmp/estest 
creating pipe: ./tmp/mtest1 
creating pipe: ./tmp/mtest2 
creating pipe: ./tmp/f1 
DSSnet -->  update b p storage post_storage 1485976509.54 estest 3 1950 2050 -500
update n p fault post_fault 1485976509.73 f1 3 1 b24 a
update n p controllable_generator post_controllable_generator 1485976509.73 gtest1 1 1.5
update b p monitor_0 post_monitor_0 1485976509.93 mtest1 0 
update b p monitor_1 post_monitor_1 1485976510.08 mtest2 0 
update n p controllable_load post_controllable_load 1485976510.23 ltest1 1 10700
update n p controllable_generator post_controllable_generator 1485976510.74 gtest1 1 1.5
update b p monitor_0 post_monitor_0 1485976511.14 mtest1 0 
update b p monitor_1 post_monitor_1 1485976511.44 mtest2 0 
update n p controllable_load post_controllable_load 1485976511.74 ltest1 1 10700
update n p controllable_generator post_controllable_generator 1485976511.74 gtest1 1 1.5
update b p monitor_0 post_monitor_0 1485976512.34 mtest1 0 
update n p controllable_generator post_controllable_generator 1485976512.74 gtest1 1 1.5
update b p monitor_1 post_monitor_1 1485976512.8 mtest2 0 
update n p controllable_load post_controllable_load 1485976513.24 ltest1 1 10700
update b p monitor_0 post_monitor_0 1485976513.55 mtest1 0 
update n p controllable_generator post_controllable_generator 1485976513.74 gtest1 1 1.5
update b p monitor_1 post_monitor_1 1485976514.15 mtest2 0 
update n p controllable_load post_controllable_load 1485976514.74 ltest1 1 10700
update n p controllable_generator post_controllable_generator 1485976514.74 gtest1 1 1.5
update b p monitor_0 post_monitor_0 1485976514.75 mtest1 0 
update b p monitor_1 post_monitor_1 1485976515.51 mtest2 0 
update n p controllable_generator post_controllable_generator 1485976515.74 gtest1 1 1.5
update b p monitor_0 post_monitor_0 1485976515.96 mtest1 0 
update n p controllable_load post_controllable_load 1485976516.24 ltest1 1 10700
update n p controllable_generator post_controllable_generator 1485976516.74 gtest1 1 1.5
update b p monitor_1 post_monitor_1 1485976516.86 mtest2 0 
update b p monitor_0 post_monitor_0 1485976517.17 mtest1 0 
update n p controllable_load post_controllable_load 1485976517.74 ltest1 1 10700
update n p controllable_generator post_controllable_generator 1485976517.74 gtest1 1 1.5
update b p monitor_1 post_monitor_1 1485976518.22 mtest2 0 
update b p monitor_0 post_monitor_0 1485976518.37 mtest1 0 
update n p controllable_generator post_controllable_generator 1485976518.74 gtest1 1 1.5
update n p controllable_load post_controllable_load 1485976519.24 ltest1 1 10700
update b p monitor_1 post_monitor_1 1485976519.58 mtest2 0 
update b p monitor_0 post_monitor_0 1485976519.59 mtest1 0 
``` 

* I hit ctrl + c and then type exit to gracefully exit the DSSnet program ( See FAQ )
```
Interrupt

Interrupt
DSSnet -->  DSSnet -->  exit
/usr/local/var/run/openvswitch/ovsdb-server.pid
dilate_all_procs -t 0 -p 1184 1182 
vagrant@coursera-sdn:~/DSSnet/net/DSSnet$ /usr/bin/java: No such file or directory
rm: cannot remove ‘/tmp/fifo.tmp’: No such file or directory
rm: cannot remove ‘*~’: No such file or directory
*** Removing excess controllers/ofprotocols/ofdatapaths/pings/noxes
killall controller ofprotocol ofdatapath ping nox_core lt-nox_core ovs-openflowd ovs-controller udpbwtest mnexec ivs 2> /dev/null
killall -9 controller ofprotocol ofdatapath ping nox_core lt-nox_core ovs-openflowd ovs-controller udpbwtest mnexec ivs 2> /dev/null
pkill -9 -f "sudo mnexec"
*** Removing junk from /tmp
rm -f /tmp/vconn* /tmp/vlogs* /tmp/*.out /tmp/*.log
*** Removing old X11 tunnels
*** Removing excess kernel datapaths
ps ax | egrep -o 'dp[0-9]+' | sed 's/dp/nl:/'
***  Removing OVS datapaths
ovs-vsctl --timeout=1 list-br
2017-02-01T19:22:01Z|00001|fatal_signal|WARN|terminating with signal 14 (Alarm clock)
Alarm clock
ovs-vsctl --timeout=1 list-br
2017-02-01T19:22:02Z|00001|fatal_signal|WARN|terminating with signal 14 (Alarm clock)
Alarm clock
*** Removing all links of the pattern foo-ethX
ip link show | egrep -o '([-_.[:alnum:]]+-eth[[:digit:]]+)'
( ip link del s1-eth2;ip link del s2-eth1;ip link del s1-eth1;ip link del s2-eth3;ip link del s3-eth1;ip link del s2-eth2;ip link del s3-eth3;ip link del s4-eth1;ip link del s3-eth2;ip link del s4-eth3;ip link del s5-eth1;ip link del s4-eth2;ip link del s5-eth4;ip link del s5-eth3;ip link del s6-eth1;ip link del s5-eth2 ) 2> /dev/null
ip link show
*** Killing stale mininet node processes
pkill -9 -f mininet:
*** Shutting down stale tunnels
pkill -9 -f Tunnel=Ethernet
pkill -9 -f .ssh/mn
rm -f ~/.ssh/mn/*
*** Cleanup complete.
 good to go! 

vagrant@coursera-sdn:~/DSSnet/net/DSSnet$ 
```

* your exact output may be different but this tests the current supported models
* controllable load
* controllable generator
* controllable energy storage (negative value for charge) 
* monitors 0 and 1
* fault
* 
* The network coordinator will keep running indefinetely. the `-et` option on the power coordinator stops the power coordinator at a set time and then exports whatever monitors were registered in the IED file. (default 2 seconds)

* This tests the blocking and non-blocking queues and verifies connectivity to the simulation. 
* __always start the power coordinator first__
* the numbers returned are time and the pmu raw measurements

## Known Issues ##
* In windows: IED file, and the load / generator 'loadshape' files are placed in C:\\DSS\DSSnet\dss\ So copy paste accordingly.
* In windows: the monitors that are exported need to be moved or they will be overwritten by subsequent experiments automatically
* when the 

## UTILITIES ##
* htop - utilizes vt information on processes
type `sudo -E htop` or just `htop` in non sudo permissions to view interesting stuff
* `ps fj` is a nice formated output to verify models are running

### Moving Forward ###
* now that the code is working you can start by creating the DSS circuit.
* create an entry for each IED (controllable load/generator/es/etc) in the IED configuration file in windows. Note IED file items are ones such that will be updated via the network coordinator.
* dynamic loads/gens go in the dss folder as csv files  ( the whole file is split evenly over the specified time (-et x))
* create an IED model (in python) for your IEDs that run in the emulation in linux
* IED models should create pipe objects similar to the example to communicate to the netCoordinator 
* create a topology and ied configuration file in linux ( use the example ones as template )
* Specify startup options and create a controller application (more to come)

### Who do I talk to? ###
To seek help, and feature requests:

* Christopher Hannon
* Channon@hawk.iit.edu
* open an issue - I'll try to help!

# Docs #

## Linux  ##

### Sync Event ###

* Synchronization events come in two varieties:
* Blocking - Will pause all hosts in network to maintain temporal accuracy
* Not blocking - Will not pause hosts in network
* see paper in PADS for more details 

#### Sync Event Format ####

* space delimited
* `update b/n destination(n/p) preprocessing_handler post_handler time hostID NumFields(n) f(1) f(2) ... f(n) `
* examples:
* update b p controllable_generator post_controllable_generator  0.1 gtest1 1 1.5
* update b p controllable_load post_controllable_load 0.2 ltest1 1 10700
* update b p monitor_0 post_monitor_0 0.45 mtest1 0
* update b p monitor_1 post_monitor_1 0.82 mtest2 0
* update b p storage post_storage 1.06 estest 3 1950 2050 -500
* update b p monitor_0 post_monitor_0 1.2 mtest1 0
* update b p monitor_1 post_monitor_1 1.4 mtest2 0
* update b p fault post_fault 1.6 f1 3 1 B24 a   


### IED Models ###

* By default all models should have a pipe from the coordinator to their process to receive messages
* For IEDs this is how they get values from the power simulator
* For other hosts it may not be necessary 
* the class to import is `pipe.py`
* the name of the pipe is `./tmp/hostid.pipe`

#### Existing Models ####
TODO
## Files ##
TODO
### IPC ###

* `pipe.py`
*  a model will call `pipe.setup_pipe(hostname)` passing in its own hostname
*  a model will call `pipe.send_sync_event(update)` to pass a synchronization event to the network coordinator
*  if a reply is expected from the synchronization event ( depending on the type of events (( see paper )) ) a call to `pipe.listen()` returns a string data if there is any data in the pipe. Typically a use would be `while i: if listen(): i=0` Im sure there are other/ better ways.


### store process metadata ###
* `DSSnet_hosts.py`
* This program contains host objects after reading in the configuration file

### sync event handler ###
* user defined synchronization preprocessing 
* post processing
* ** This file determines how models will interface with power coordinator **
todo - add more description

## Configs ##

### IED config ###

* contains the information for starting the models in the network emulator
* field 1 is unique identifier for the id of the host
* field 2 is a description of the host 
* field 3 is the assigned ip address
* field 4 is the startup command for the host - can use && |& ; etc
* keyword split is used to deliminate the field
* TODO use better config formats

#### format ####
* id split msg split ip split command
* `PMU101 split PMU split 1.2.3.4 split python pmu.py 101 pdc5 1.4.2.5 pmu101 > log.txt`

### topo config ###
* defines switches links and linkops

#### format ####
* new switch_id
* a b linkops

## FAQ ##

1.) Freezes upon starting host processes   
ans:  Common problem: dont forget the `&` so that the process on hosts run in background.      
2.) netCoord.py appears black after typeing exit    
ans: poor thread management. hit ctrl + c and probably will experience issue 3  
3.) after exiting netCoord.py I can not see cursor ( or typing text in terminal) anymore  
ans:  hit ctrl + c in terminal window then type `sudo netCoord.py -c`    


## Troubleshooting ##

I get an error: Exception Please shut down the controller which is running on port 6653?

```
sudo python netCoord.py 
Opening Connection to tcp://10.47.142.26:50021
*** Creating network
*** Adding controller
Traceback (most recent call last):
  File "netCoord.py", line 291, in <module>
    run_main()
  File "netCoord.py", line 256, in run_main
    net = Mininet(top, link = TCLink)
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 172, in __init__
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 444, in build
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 411, in buildFromTopo
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 261, in addController
  File "build/bdist.linux-x86_64/egg/mininet/node.py", line 1539, in DefaultController
  File "build/bdist.linux-x86_64/egg/mininet/node.py", line 1362, in __init__
  File "build/bdist.linux-x86_64/egg/mininet/node.py", line 1380, in checkListening
Exception: Please shut down the controller which is running on port 6653:
Active Internet connections (servers and established)
tcp        0      0 127.0.0.1:52615         127.0.0.1:6653          TIME_WAIT   -               
tcp        0      0 127.0.0.1:52618         127.0.0.1:6653          TIME_WAIT   -               
tcp6       0      0 :::6653                 :::*                    LISTEN      22734/java      
```

Well you should reserve this port for the controller. 
