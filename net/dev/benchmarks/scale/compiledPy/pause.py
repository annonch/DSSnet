import time
import logging
import os
import sys
import subprocess

log = 'log.log'
logging.basicConfig(filename=log,level=logging.DEBUG)


def pause (NPAUSE):
    before_time = time.time()
    process = subprocess.call(NPAUSE,shell=True)
    after_time = time.time()
    logging.info('pause,%s'% (after_time-before_time))


def resume (NRESUME):
    before_time = time.time()
    process = subprocess.call(NRESUME,shell=True)
    after_time = time.time()
    logging.info('resume,%s'% (after_time-before_time))
