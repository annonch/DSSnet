import sys
import matplotlib.pyplot as plt
import numpy as np
osFile = sys.argv[1] 
suFile = sys.argv[2] 


os = np.loadtxt(osFile)# with pause
su = np.loadtxt(suFile)

# sort the data:
os_sorted = np.sort(os)# paused
su_sorted = np.sort(su)


# calculate the proportional values of samples
pos = 1. * np.arange(len(os)) / (len(os) - 1) #paused
psu = 1. * np.arange(len(su)) / (len(su) -1)

# plot the sorted data:
fig = plt.figure()

ax1 = fig.add_subplot(121)#121
#ax1.axis([0, 20, 0, 1])
ax1.set_title('psub_red_vs_os_blue')
ax1.plot(os_sorted,pos,color='b')
ax1.set_xlabel('$rtt-ms$')
ax1.set_ylabel('$p$')
ax1.plot(su_sorted,psu,color='r')
'''
ax2 = fig.add_subplot(122)#121
ax2.axis([float(sys.argv[3]),
          float(sys.argv[4]),
          float(sys.argv[5]),
          float(sys.argv[6])])
ax2.set_title('pause_red_vs_noPause_blue')
ax2.plot(bl_sorted,pbl,color='b')
ax2.set_xlabel('$rtt-ms$')
ax2.set_ylabel('$p$')
ax2.plot(vt_sorted,pvt,color='r')
'''

plt.show()
