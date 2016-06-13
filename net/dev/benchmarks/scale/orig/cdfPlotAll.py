#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np
import six
import matplotlib.colors as colors
import matplotlib

def plot_scale(scale):
    global cnt

    freezeData = np.loadtxt("freeze_%s.txt" % scale)
    unfreezeData = np.loadtxt("unfreeze_%s.txt" % scale)
    freezeData *= 1000 # to milliseconds
    unfreezeData *= 1000
    data = freezeData + unfreezeData    
    num_bins = 1000
    counts, bin_edges = np.histogram(data, bins=num_bins)
    cdf = np.cumsum(counts) * 1.0 / (len(data) - 1)
    plt.plot(bin_edges[1:], cdf, color=colors_name[cnt], linestyle=ls_name[cnt], linewidth=3.5, label='%d Hosts' % scale)
    cnt += 1

def plot_all(output_file):
    global cnt
    matplotlib.rc('font', size=15)
    plt.figure()
    for scale in [10, 50, 100, 250, 500]:
        plot_scale(scale) 

    plt.grid(True)
    plt.xticks(range(0, 251, 25))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('Emulation Overhead (Milliseconds)', fontsize=20)
    plt.ylabel('Cumulative Distribution', fontsize=20)
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.ylim([0, 1.01]) 
    plt.savefig(output_file, format='eps')

if __name__ == '__main__':
    cnt = 0
    ls_name = ['solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':']
    colors_ = list(six.iteritems(colors.cnames))
    colors_name = [x[0] for x in colors_]
    colors_name = ['red', 'blue', 'cyan', 'purple', 'green', 'salmon', 'pink', 'lime', 'tan', 'seagreen', 'peru', 'wheat']
    print colors_name
    output = 'ScaleFrzCDF.eps'
    plot_all(output)


