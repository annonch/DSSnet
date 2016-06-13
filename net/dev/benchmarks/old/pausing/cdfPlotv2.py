
import matplotlib.pyplot as plt
import numpy as np

data3= np.loadtxt('filename.3sPause.txt')
data = np.loadtxt('Filename.txt')# with pause
data2 = np.loadtxt('Filenamewop.txt')

# sort the data:
data_sorted = np.sort(data)
data2_sorted = np.sort(data2)
data3_sorted = np.sort(data3)

# calculate the proportional values of samples
p = 1. * np.arange(len(data)) / (len(data) - 1)
p2 = 1. * np.arange(len(data2)) / (len(data2) -1)
p3 = 1. * np.arange(len(data3)) / (len(data3) -1)

# plot the sorted data:
fig = plt.figure()

ax1 = fig.add_subplot(121)
ax1.set_title('pause_.3s_red_vs_noPause_blue')
ax1.plot(data2_sorted,p2,color='b')
ax1.set_xlabel('$rtt-ms$')
ax1.set_ylabel('$p$')
ax1.plot(data3_sorted,p3,color='r')


ax2 = fig.add_subplot(122)
ax2.plot(data_sorted, p, color = 'r')
ax2.set_title('pause_1s_red_vs_noPause_blue')
ax2.set_xlabel('$round-trip-time-in-ms$')
ax2.set_ylabel('$p$')

ax2.plot(data2_sorted, p2, color='b')

plt.show()
