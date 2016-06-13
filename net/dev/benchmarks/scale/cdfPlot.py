#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np
data1File = sys.argv[1]
data2File = sys.argv[2]
output_file = sys.argv[3]

data1 = np.loadtxt(data1File)
data2 = np.loadtxt(data2File)

# sort the data:
data1_sorted = np.sort(data1)
data2_sorted = np.sort(data2)

# calculate the proportional values of samples
pdata1 = 1. * np.arange(len(data1)) / (len(data1) - 1)
pdata2 = 1. * np.arange(len(data2)) / (len(data2) - 1)

# plot the sorted data:
fig = plt.figure()

# ax1.set_title('Freeze/Unfreeze Overhead')
plt.plot(data1_sorted, pdata1, color='b', label='freeze')
plt.plot(data2_sorted, pdata2, color='r', label='unfreeze')
plt.legend(loc='lower right')
plt.xlabel('$Time\ Elapsed / Microseconds$')
plt.ylabel('$Cumulative\ Distribution$')
plt.grid(True)

plt.savefig(output_file, format='eps')


