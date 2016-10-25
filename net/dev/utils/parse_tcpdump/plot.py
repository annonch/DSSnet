#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import math

# 6 x's 

base_x_down = np.loadtxt('base_x_down.txt')
base_x_up = np.loadtxt('base_x_up.txt')

no_ovs_vt_x_downt = np.loadtxt('no_ovs_vt_x_down.txt')
no_ovs_vt_x_down = [x/2 for x in no_ovs_vt_x_downt]
no_ovs_vt_x_upt = np.loadtxt('no_ovs_vt_x_up.txt')
no_ovs_vt_x_up = [x/2 for x in no_ovs_vt_x_upt]

vt_x_down = np.loadtxt('vt_x_down.txt')
vt_x_up = np.loadtxt('vt_x_up.txt')

fig = plt.figure()
ax1= fig.add_subplot(111)
ax1.axis([0,7,0,60])
ax1.set_title('Effect of Virtual Time on STP Convergence')

size = len(base_x_down)
print size
mean = sum(base_x_down)/size
print mean
stds = np.std(base_x_down)
print stds
ax1.errorbar(1,mean,yerr = (stds/math.sqrt(size))*1.96,color='black', linewidth = 2)

size = len(base_x_up)
print size
mean = sum(base_x_up)/size
print mean
stds = np.std(base_x_up)
print stds
ax1.errorbar(2,mean, yerr = (stds/math.sqrt(size))*1.96,color='black', linewidth = 2)

size = len(no_ovs_vt_x_down)
print size
mean = sum(no_ovs_vt_x_down)/size
print mean
stds = np.std(no_ovs_vt_x_down)
print stds
ax1.errorbar(3,mean, yerr = (stds/math.sqrt(size))*1.96,color='black', linewidth = 2)

size = len(no_ovs_vt_x_up)
print size
mean = sum(no_ovs_vt_x_up)/size
print mean
stds = np.std(no_ovs_vt_x_up)
print stds
ax1.errorbar(4,mean, yerr = (stds/math.sqrt(size))*1.96,color='black', linewidth = 2)

size = len(vt_x_down)
print size
mean = sum(vt_x_down)/size
print mean
stds = np.std(vt_x_down)
print stds
ax1.errorbar(5,mean, yerr = (stds/math.sqrt(size))*1.96,color='black', linewidth = 2)

size = len(vt_x_up)
print size
mean = sum(vt_x_up)/size
print mean
stds = np.std(vt_x_up)
print stds
ax1.errorbar(6,mean, yerr = (stds/math.sqrt(size))*1.96,color='black', linewidth = 2)

my_xticks = [' ','Link Down\nBase Case','Link Up\nBase Case', 'Link Down\n ovs not in vt', 'Link Up\n ovs not in vt','Link Down\n ovs in vt', 'Link Up\n ovs in vt',' ']

labels = [item.get_text() for item in ax1.get_xticklabels()]
print labels
labels = my_xticks

ax1.set_xticklabels(my_xticks, rotation=30)

ax1.set_ylabel('Convergence Time (Seconds)')

plt.show()
