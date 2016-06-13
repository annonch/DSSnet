mkdir /cpuset 
mount -t cpuset none /cpuset/
cd /cpuset

mkdir sys                                   # create sub-cpuset for system processes
/bin/echo 0-2 > sys/cpuset.cpus             # assign cpus (cores) 0-2 to this set
                                            # adjust if you have more/less cores
/bin/echo 1 > sys/cpuset.cpu_exclusive
/bin/echo 0 > sys/cpuset.mems     

mkdir rt                                    # create sub-cpuset for my process
/bin/echo 3 > rt/cpuset.cpus                # assign cpu (core) 3 to this cpuset
                                            # adjust this to number of cores-1
/bin/echo 1 > rt/cpuset.cpu_exclusive
/bin/echo 0 > rt/cpuset.mems
/bin/echo 0 > rt/cpuset.sched_load_balance
/bin/echo 1 > rt/cpuset.mem_hardwall

# move all processes from the default cpuset to the sys-cpuset
for T in `cat tasks`; do echo "Moving " $T; /bin/echo $T > sys/tasks; done
