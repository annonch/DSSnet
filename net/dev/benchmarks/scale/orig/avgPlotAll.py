#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np
import six
import matplotlib.colors as colors
import matplotlib
import math

def plot_all(output_file):
    plt.figure()
    avg = []
    std = []
    conf_int = []

    scales = [10, 50, 100, 250, 500]
    for scale in scales:
        freezeData = np.loadtxt("freeze_%s.txt" % scale)
        unfreezeData = np.loadtxt("unfreeze_%s.txt" % scale)
        size = len(freezeData)
        freezeData *= 1000 # to milliseconds
        unfreezeData *= 1000 
        sync = np.add(freezeData, unfreezeData) 
        avg.append(np.average(sync))
        std.append(np.std(sync))
        conf_int.append(np.std(sync) * 1.96 / math.sqrt(size))
        
    matplotlib.rc('font', size=15)
    plt.plot(scales, avg, color='blue', linewidth=2.0, label='Emulation Overhead') 
    plt.bar(scales, avg, width=35, color='white', yerr=std, ecolor='red', hatch='/')
 
    plt.grid(True)
    plt.xticks([10,50,100,150,200,250,300,350,400,450,500,550], horizontalalignment='left')
    plt.xlabel('Number of Hosts', fontsize=20)
    plt.ylabel('Average Overhead (Milliseconds)', fontsize=20)
    plt.legend(loc='upper left')

    plt.savefig(output_file, format='eps')
    plt.show()

if __name__ == '__main__':
    ls_name = ['solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':']
    colors_name = ['red', 'blue', 'cyan', 'peru', 'green', 'salmon', 'pink', 'lime', 'tan', 'seagreen', 'purple', 'wheat']
    print colors_name
    output = 'ScaleFrzAvg.eps'
    plot_all(output)



