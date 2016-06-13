
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.patches as mpatches


data = np.loadtxt('pause.test')# with pause
data2 = np.loadtxt('noPause.test')

# sort the data:
data_sorted = np.sort(data)# paused
data2_sorted = np.sort(data2)


# calculate the proportional values of samples
p = 1. * np.arange(len(data)) / (len(data) - 1) #paused
p2 = 1. * np.arange(len(data2)) / (len(data2) -1)

# plot the sorted data:
fig = plt.figure()

ax1 = fig.add_subplot(121)#121
#ax1.axis([75, 225, 0, 1])
ax1.set_title('Ping test on 10 switch linear topology - 2ms delay')
ax1.plot(data2_sorted,p2,color='b',label="normal")
ax1.set_xlabel('$rtt-ms$')
ax1.set_ylabel('$p$')
ax1.plot(data_sorted,p,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax1.get_legend().get_title().set_color("red")


ax2 = fig.add_subplot(122)#121
ax2.axis([440, 550, 0.25, 0.4])
ax2.set_title('pause_red_vs_noPause_blue')
ax2.plot(data2_sorted,p2,color='b',label="normal")
ax2.set_xlabel('$rtt-ms$')
ax2.set_ylabel('$p$')
ax2.plot(data_sorted,p,color='r',label="with Pause")
plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax2.get_legend().get_title().set_color("red")

plt.show()
