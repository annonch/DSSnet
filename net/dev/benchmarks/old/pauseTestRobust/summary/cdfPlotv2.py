#!/usr/bin/python
####################
#  channon@iit.edu # 
####################

# benchmarking summary for pause algorithm
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 12})

# row 1 delay = 20 ms: 
#    1 switch | 10 switches | 100 switches | 2 switches w/ 100 bg hosts
# row 2 delay = 2 ms: 
#    1 switch | 10 switches | 100 switches | 2 switches w/ 100 bg hosts
#

row1col1a= np.loadtxt('../20msDelay/1s/pause.test')# with pause
row1col1b = np.loadtxt('../20msDelay/1s/noPause.test')
row1col2a= np.loadtxt('../20msDelay/10s/pause.test')# with pause
row1col2b = np.loadtxt('../20msDelay/10s/noPause.test')
row1col3a= np.loadtxt('../20msDelay/100s/pause.test')# with pause
row1col3b = np.loadtxt('../20msDelay/100s/noPause.test')
row1col4a= np.loadtxt('../20msDelay/100s-bg/pause.test')# with pause
row1col4b = np.loadtxt('../20msDelay/100s-bg/noPause.test')

row2col1a= np.loadtxt('../2msDelay/1s/pause.test')# with pause
row2col1b = np.loadtxt('../2msDelay/1s/noPause.test')
row2col2a= np.loadtxt('../2msDelay/10s/pause.test')# with pause
row2col2b = np.loadtxt('../2msDelay/10s/noPause.test')
row2col3a= np.loadtxt('../2msDelay/100s/pause.test')# with pause
row2col3b = np.loadtxt('../2msDelay/100s/noPause.test')
row2col4a= np.loadtxt('../2msDelay/100s-bg/pause.test')# with pause
row2col4b = np.loadtxt('../2msDelay/100s-bg/noPause.test')

row3col1a= np.loadtxt('../lowbw2msDelay/1s/pause.test')# with pause
row3col1b = np.loadtxt('../lowbw2msDelay/1s/noPause.test')
row3col2a= np.loadtxt('../lowbw2msDelay/10s/pause.test')# with pause
row3col2b = np.loadtxt('../lowbw2msDelay/10s/noPause.test')
row3col3a= np.loadtxt('../lowbw2msDelay/100s/pause.test')# with pause
row3col3b = np.loadtxt('../lowbw2msDelay/100s/noPause.test')
row3col4a= np.loadtxt('../lowbw2msDelay/100s-bg/pause.test')# with pause
row3col4b = np.loadtxt('../lowbw2msDelay/100s-bg/noPause.test')

# sort the data:
row1col1a_sorted = np.sort(row1col1a)# paused
row1col1b_sorted = np.sort(row1col1b)
row1col2a_sorted = np.sort(row1col2a)# paused
row1col2b_sorted = np.sort(row1col2b)
row1col3a_sorted = np.sort(row1col3a)# paused
row1col3b_sorted = np.sort(row1col3b)
row1col4a_sorted = np.sort(row1col4a)# paused
row1col4b_sorted = np.sort(row1col4b)

row2col1a_sorted = np.sort(row2col1a)# paused
row2col1b_sorted = np.sort(row2col1b)
row2col2a_sorted = np.sort(row2col2a)# paused
row2col2b_sorted = np.sort(row2col2b)
row2col3a_sorted = np.sort(row2col3a)# paused
row2col3b_sorted = np.sort(row2col3b)
row2col4a_sorted = np.sort(row2col4a)# paused
row2col4b_sorted = np.sort(row2col4b)

row3col1a_sorted = np.sort(row3col1a)# paused
row3col1b_sorted = np.sort(row3col1b)
row3col2a_sorted = np.sort(row3col2a)# paused
row3col2b_sorted = np.sort(row3col2b)
row3col3a_sorted = np.sort(row3col3a)# paused
row3col3b_sorted = np.sort(row3col3b)
row3col4a_sorted = np.sort(row3col4a)# paused
row3col4b_sorted = np.sort(row3col4b)


# calculate the proportional values of samples
p = 1. * np.arange(len(row1col1a)) / (len(row1col1a) - 1) #paused
p2 = 1. * np.arange(len(row1col1b)) / (len(row1col1b) -1)
p3= 1. * np.arange(len(row1col2a)) / (len(row1col2a) - 1) #paused
p4 = 1. * np.arange(len(row1col2b)) / (len(row1col2b) -1)
p5= 1. * np.arange(len(row1col3a)) / (len(row1col3a) - 1) #paused
p6 = 1. * np.arange(len(row1col3b)) / (len(row1col3b) -1)
p7= 1. * np.arange(len(row1col4a)) / (len(row1col4a) - 1) #paused
p8 = 1. * np.arange(len(row1col4b)) / (len(row1col4b) -1)

p9 = 1. * np.arange(len(row2col1a)) / (len(row2col1a) - 1) #paused
p10= 1. * np.arange(len(row2col1b)) / (len(row2col1b) -1)
p11= 1. * np.arange(len(row2col2a)) / (len(row2col2a) - 1) #paused
p12= 1. * np.arange(len(row2col2b)) / (len(row2col2b) -1)
p13= 1. * np.arange(len(row2col3a)) / (len(row2col3a) - 1) #paused
p14= 1. * np.arange(len(row2col3b)) / (len(row2col3b) -1)
p15= 1. * np.arange(len(row2col4a)) / (len(row2col4a) - 1) #paused
p16= 1. * np.arange(len(row2col4b)) / (len(row2col4b) -1)

p17 = 1. * np.arange(len(row3col1a)) / (len(row3col1a) - 1) #paused
p18= 1. * np.arange(len(row3col1b)) / (len(row3col1b) -1)
p19= 1. * np.arange(len(row3col2a)) / (len(row3col2a) - 1) #paused
p20= 1. * np.arange(len(row3col2b)) / (len(row3col2b) -1)
p21= 1. * np.arange(len(row3col3a)) / (len(row3col3a) - 1) #paused
p22= 1. * np.arange(len(row3col3b)) / (len(row3col3b) -1)
p23= 1. * np.arange(len(row3col4a)) / (len(row3col4a) - 1) #paused
p24= 1. * np.arange(len(row3col4b)) / (len(row3col4b) -1)

# plot the sorted data:
fig = plt.figure()

ax1 = fig.add_subplot(341)#121
ax1.axis([75, 180, 0, 1])
ax1.set_title('20ms Delay|10mb Ping Test: 1 switch linear')
ax1.plot(row1col1b_sorted,p2,color='b',label="normal")
ax1.set_xlabel('$rtt-ms$')
ax1.set_ylabel('$p$')
ax1.plot(row1col1a_sorted,p,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax1.get_legend().get_title().set_color("red")
#
ax2 = fig.add_subplot(342)#121
ax2.axis([425, 800, 0, 1])
ax2.set_title('20ms Delay|10mb Ping Test: 10 switch linear')
ax2.plot(row1col2b_sorted,p4,color='b',label="normal")
ax2.set_xlabel('$rtt-ms$')
ax2.set_ylabel('$p$')
ax2.plot(row1col2a_sorted,p3,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax2.get_legend().get_title().set_color("red")
#
ax3 = fig.add_subplot(343)#121
ax3.axis([4000, 5500, 0, 1])
ax3.set_title('20ms Delay|10mb Ping Test: 100 switch linear')
ax3.plot(row1col3b_sorted,p6,color='b',label="normal")
ax3.set_xlabel('$rtt-ms$')
ax3.set_ylabel('$p$')
ax3.plot(row1col3a_sorted,p5,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax3.get_legend().get_title().set_color("red")
#
ax4 = fig.add_subplot(344)#121
ax4.axis([120, 180, 0, 1])
ax4.set_title('20ms Delay|10mb Ping Test: 2 switch linear- 100 bg hosts')
ax4.plot(row1col4b_sorted,p8,color='b',label="normal")
ax4.set_xlabel('$rtt-ms$')
ax4.set_ylabel('$p$')
ax4.plot(row1col4a_sorted,p7,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax4.get_legend().get_title().set_color("red")





ax5 = fig.add_subplot(345)#121
ax5.axis([0, 40, 0, 1])
ax5.set_title('2ms Delay|10mb Ping Test: 1 switch linear')
ax5.plot(row2col1b_sorted,p10,color='b',label="normal")
ax5.set_xlabel('$rtt-ms$')
ax5.set_ylabel('$p$')
ax5.plot(row2col1a_sorted,p9,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax5.get_legend().get_title().set_color("red")
#
ax6 = fig.add_subplot(346)#121
ax6.axis([20, 400, 0, 1])
ax6.set_title('2ms Delay|10mb Ping Test: 10 switch linear')
ax6.plot(row2col2b_sorted,p12,color='b',label="normal")
ax6.set_xlabel('$rtt-ms$')
ax6.set_ylabel('$p$')
ax6.plot(row2col2a_sorted,p11,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax6.get_legend().get_title().set_color("red")
#
ax7 = fig.add_subplot(347)#121
ax7.axis([400, 2000, 0, 1])
ax7.set_title('2ms Delay|10mb Ping Test: 100 switch linear')
ax7.plot(row2col3b_sorted,p14,color='b',label="normal")
ax7.set_xlabel('$rtt-ms$')
ax7.set_ylabel('$p$')
ax7.plot(row2col3a_sorted,p13,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax7.get_legend().get_title().set_color("red")
#
ax8 = fig.add_subplot(348)#121
ax8.axis([10, 60, 0, 1])
ax8.set_title('2ms Delay|10mb Ping Test: 2 switch linear- 100 bg hosts')
ax8.plot(row2col4b_sorted,p16,color='b',label="normal")
ax8.set_xlabel('$rtt-ms$')
ax8.set_ylabel('$p$')
ax8.plot(row2col4a_sorted,p15,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax8.get_legend().get_title().set_color("red")

#########

ax9 = fig.add_subplot(349)#121
ax9.axis([0, 40, 0, 1])
ax9.set_title('2ms Delay|1mb Ping Test: 1 switch linear')
ax9.plot(row3col1b_sorted,p18,color='b',label="normal")
ax9.set_xlabel('$rtt-ms$')
ax9.set_ylabel('$p$')
ax9.plot(row3col1a_sorted,p17,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax9.get_legend().get_title().set_color("red")
#
ax10 = fig.add_subplot(3,4,10)#121
ax10.axis([20, 400, 0, 1])
ax10.set_title('2ms Delay|1mb Ping Test: 10 switch linear')
ax10.plot(row3col2b_sorted,p20,color='b',label="normal")
ax10.set_xlabel('$rtt-ms$')
ax10.set_ylabel('$p$')
ax10.plot(row3col2a_sorted,p19,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax10.get_legend().get_title().set_color("red")
#
ax11 = fig.add_subplot(3,4,11)#121
ax11.axis([400, 2000, 0, 1])
ax11.set_title('2ms Delay|1mb Ping Test: 100 switch linear')
ax11.plot(row3col3b_sorted,p22,color='b',label="normal")
ax11.set_xlabel('$rtt-ms$')
ax11.set_ylabel('$p$')
ax11.plot(row3col3a_sorted,p21,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax11.get_legend().get_title().set_color("red")
#
ax12 = fig.add_subplot(3,4,12)#121
ax12.axis([10, 60, 0, 1])
ax12.set_title('2ms Delay|1mb Ping Test: 2 switch linear- 100 bg hosts')
ax12.plot(row3col4b_sorted,p24,color='b',label="normal")
ax12.set_xlabel('$rtt-ms$')
ax12.set_ylabel('$p$')
ax12.plot(row3col4a_sorted,p23,color='r',label="with Pause") # pause

plt.legend(loc="lower right", 
           shadow=True, title="Legend", fancybox=True)
ax12.get_legend().get_title().set_color("red")


plt.show()
