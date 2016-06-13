import sys
import matplotlib.pyplot as plt
import numpy as np
vtFile = sys.argv[1] 
blFile = sys.argv[2] 

vt = np.loadtxt(vtFile)# with pause
bl = np.loadtxt(blFile)

# sort the data:
vt_sorted = np.sort(vt)# paused
bl_sorted = np.sort(bl)


# calculate the proportional values of samples
pvt = 1. * np.arange(len(vt)) / (len(vt) - 1) #paused
pbl = 1. * np.arange(len(bl)) / (len(bl) -1)

# plot the sorted data:
fig = plt.figure()

ax1 = fig.add_subplot(121)#121
ax1.axis([0, 0.5, 0, 1])
ax1.set_title('pause_red_vs_noPause_blue')
ax1.plot(bl_sorted,pbl,color='b')
ax1.set_xlabel('$rtt-ms$')
ax1.set_ylabel('$p$')
ax1.plot(vt_sorted,pvt,color='r')

ax2 = fig.add_subplot(122)#121
ax2.axis([0.1, 0.5, 0.4, 1])
ax2.set_title('pause_red_vs_noPause_blue')
ax2.plot(bl_sorted,pbl,color='b')
ax2.set_xlabel('$rtt-ms$')
ax2.set_ylabel('$p$')
ax2.plot(vt_sorted,pvt,color='r')


plt.show()
