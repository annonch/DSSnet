#!usr/bin/python

import time
import subprocess


PAUSE  ="sudo pgrep -f mininet: | sudo awk  \'{system(\"sudo kill --signal SIGSTOP -\"$1)}' -"
RESUME ="sudo pgrep -f mininet: | sudo awk  \'{system(\"sudo kill --signal SIGCONT -\"$1)}' -"

def test():
    process = subprocess.call(PAUSE, shell=True)
    process = subprocess.call(RESUME, shell=True)
