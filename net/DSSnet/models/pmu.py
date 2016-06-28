#!/usr/bin/python3.4
#####################
#  channon@iit.edu  #
#####################

#pmu.py

import pipes
import time
import sys

pipeout = pipe.setup_pipe_l(sys.argv[1])
pipin = pipe.setup_pipe_w()

from ctypes import *
#from numpy import array

libpmu=cdll.LoadLibrary('./libpmu.so')

class PMU:

    def __init__(self, idcode, message_time_quality,
                 stn, data_format, phnmr,
                 annmr, dgnmr, chnam, phunit, anunit, digunit,
                 fnom, cfgcnt, data_rate, time_base, pdc_IP, pdc_port):
        self.idcode               = idcode
        self.message_time_quality = message_time_quality
        self.time_base            = time_base
        self.stn                  = stn
        self.data_format          = data_format
        self.phnmr                = phnmr
        self.annmr                = annmr
        self.dgnmr                = dgnmr
        self.chnam                = chnam
        self.phunit               = phunit
        self.anunit               = anunit
        self.digunit              = digunit
        self.fnom                 = fnom
        self.cfgcnt               = cfgcnt
        self.data_rate            = data_rate
        self.pdc_IP               = pdc_IP
        self.pdc_port             = pdc_port

def prnt(p):
    print (p.idcode)
    print (p.message_time_quality)
    print (p.time_base)
    print (p.stn)
    print (p.data_format)
    print (p.phnmr)
    print (p.annmr)
    print (p.dgnmr)
    print (p.chnam)
    print (p.phunit)
    print (p.anunit)
    print (p.digunit)
    print (p.fnom)
    print (p.cfgcnt)
    print (p.data_rate)
    print (p.pdc_IP)
    print (p.pdc_port)


def _cfg2(pmu):
    #//print('hi0\n\n')
    libpmu.cfg2_python(c_int(pmu.pdc_port),
                       c_int(pmu.idcode),
                       c_int(pmu.message_time_quality),
                       c_int(pmu.data_format),
                       c_char_p(pmu.stn),
                       c_int(pmu.phnmr),
                       c_int(pmu.annmr),
                       c_int(pmu.dgnmr),
                       (c_char_p(pmu.chnam)),
                       (pmu.phunit),
                       (pmu.anunit),
                       (pmu.digunit),
                       c_int(pmu.fnom),
                       c_int(pmu.cfgcnt),
                       c_int(pmu.data_rate),
                       c_int(pmu.time_base),
                       c_char_p(pmu.pdc_IP)
                       )

def _data(pmu, phasor_data, analog_data, digital_data, freq_data, dfreq_data):
    libpmu.data_python(c_int(pmu.pdc_port),
                       c_int(pmu.idcode),
                       c_int(pmu.message_time_quality),
                       c_int(pmu.data_format),
                       c_char_p(pmu.stn),
                       c_int(pmu.phnmr),
                       c_int(pmu.annmr),
                       c_int(pmu.dgnmr),
                       (c_char_p(pmu.chnam)),
                       (pmu.phunit),
                       (pmu.anunit),
                       (pmu.digunit),
                       c_int(pmu.fnom),
                       c_int(pmu.cfgcnt),
                       c_int(pmu.data_rate),
                       c_int(pmu.time_base),
                       c_char_p(pmu.pdc_IP),
                       phasor_data,
                       analog_data,
                       digital_data,
                       freq_data,
                       dfreq_data
                       )






def read_pmu(filename):
    with open(filename, 'r') as config:
        phnmr = 0
        annmr = 0
        dgnmr = 0
        data_format = 0
        chna = ''
        fnom = 0
        message_time_quality = 0
        phuni = []
        anuni = []
        diguni = []

        for line in config:
            line_split = line.split(',')
            if line_split[0] == 'idcode':
                idcode=int(line_split[1])
            elif line_split[0] == 'stn':
                stn = line_split[1].encode('utf-8')
            elif line_split[0] == 'phnmr':
                phnmr = int(line_split[1])
            elif line_split[0] == 'annmr':
                annmr = int(line_split[1])
            elif line_split[0] == 'dgnmr':
                dgnmr = int(line_split[1])
            elif line_split[0] == 'chnam':
                for x in range(1,1+dgnmr*16+annmr+phnmr):
                    new_d = pad(line_split[x],16)
                    chna += new_d
                chnam = chna.encode('utf-8')
            elif line_split[0] == 'fnom':
                if line_split[1] == '50':
                    fnom = 1
            elif line_split[0] == 'ip':
                IP = line_split[1].encode('utf-8')
            elif line_split[0] == 'data_format':
                if line_split[1] == 'float':
                    data_format += 8
                if line_split[2] == 'float':
                    data_format += 4
                if line_split[3] == 'float':
                    data_format += 2
                if line_split[4] == 'polar':
                    data_format += 1
            elif line_split[0] == 'port':
                port = ((line_split[1]))
            elif line_split[0] == 'phunit':
                for x in range(1,phnmr+1):
                    phuni.append(c_int(int(line_split[x])))
            elif line_split[0] == 'anunit':
                for x in range(1,annmr+1):
                    anuni.append(c_int(int(line_split[x])))
            elif line_split[0] == 'digunit':
                for x in range(1,dgnmr+1):
                    diguni.append(c_int(int(line_split[x])))
            elif line_split[0] == 'cfgcnt':
                cfgcnt = int(line_split[1])
            elif line_split[0] == 'data_rate':
                data_rate = int(line_split[1])
            elif line_split[0] == 'time_base':
                time_base = int(line_split[1])

    phunit = (c_int*len(phuni))(*phuni)
    anunit = (c_int*len(anuni))(*anuni)
    digunit = (c_int*len(diguni))(*diguni)

    pmu = PMU(idcode, message_time_quality,
                 stn, data_format, phnmr,
                 annmr, dgnmr, chnam, phunit, None, None,
                 fnom, cfgcnt, data_rate, time_base, IP, 4712)

    return pmu

def data_process(raw_data, pmu):#phnmr, annmr, dgnmr, freq, dfreq):
    data = raw_data.split()

    phasor_data = []
    analog_data = []
    digital_data = []

    for x in range(0, pmu.phnmr*2):
        phasor_data.append(float(data[x]))
    for x in range(pmu.phnmr*2, pmu.phnmr *2 + pmu.annmr):
        analog_data.append(float(data[x]))
    for x in range(pmu.phnmr *2 + pmu.annmr, pmu.phnmr*2 + pmu.annmr + pmu.dgnmr):
        digital_data.appendfloat((data[x]))

    freq = float(data[pmu.phnmr*2+pmu.annmr+pmu.dgnmr])
    dfreq = float(data[pmu.phnmr*2+pmu.annmr+pmu.dgnmr+1])


    ph_data = (c_float*len(phasor_data))(*phasor_data)
    an_data = (c_float*len(analog_data))(*analog_data)
    dg_data = (c_float*len(digital_data))(*digital_data)

    freq_data = (c_float)(freq)
    dfreq_data = (c_float)(dfreq)
    return ph_data, an_data, dg_data, freq_data, dfreq_data

def pad(d,size):
    data=d
    room = size-len(data)
    if room > 0:
        for x in range(room):
            data+=' '
    elif room < 0:
        data=data[:(abs(room))]
    return data

 #scheduler function
 def do_every(interval, worker_func, iterations = 0):
     if iterations !=1:
         threading.Timer (
             interval,
             do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
         ).start();
         worker_func();

def request_data():
    pipe.send_sync_event('update b p pre_pmu post_pmu %s a1 0\n'% time.time(), pipin)


pmu = read_pmu('pmu.config')

_cfg2(pmu)


do_every(0.3,request_data)

while 1:
    if raw_message=pipe.listen(pipout):
        message=raw_message[0]
        if message[0] == 'cfg2':
            _cfg2(pmu)
        else:
            raw_data = raw_message
            #raw_data = '7199.36 0.1 7199.37 -2.27 7199.36 2.27 334.51 -0.6225 59.9 0.01'
            phasor_data, analog_data, digital_data, freq_data, dfreq_data = data_process(raw_data,pmu)
            _data(pmu, phasor_data, analog_data, digital_data, freq_data, dfreq_data)
