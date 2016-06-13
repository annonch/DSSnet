#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np
import six
import matplotlib.colors as colors
# import matplotlib.markers.MarkerStyle as ms

def plot_all(output_file):
    global cnt
    
    loadShiftData = np.loadtxt("LoadShiftData.txt")[:9000]
    loadShiftTimeData=np.loadtxt("LoadShiftTimeData.txt")[:9000]
    loadShiftTimeData = loadShiftTimeData[:8850]
    loadShiftData = loadShiftData[:8850]
    noLoadShiftData= np.loadtxt("noLoadShiftData.txt")
    noLoadShiftTimeData=np.loadtxt("noLoadShiftTimeData.txt")
    noLoadShiftTimeData = noLoadShiftTimeData[:9350]
    noLoadShiftData = noLoadShiftData[:9350]
    DoSData= np.loadtxt("DoSData.txt")
    DoSTimeData=np.loadtxt("DoSTimeData.txt")
    DoSTimeData = DoSTimeData[:9350]
    DoSData = DoSData[:9350]
    utilityData= np.loadtxt("utilityData2.txt")
    utilityTimeData=np.loadtxt("utilityTimeData2.txt")
 
    f, ax = plt.subplots()

    ax.plot(loadShiftTimeData, loadShiftData, color='red', linewidth=2.0, label='Load Shifting')
    cnt += 1
    ax.plot(noLoadShiftTimeData, noLoadShiftData, color='blue', ls='dashed', linewidth=2.0, label='Without Load Shifting')
    cnt += 1
    ax.plot(DoSTimeData, DoSData, color='green', ls='dashdot', linewidth=3.0, label='DoS Attack')
    cnt += 1
    ax.plot(utilityTimeData, utilityData, color='purple', ls='dotted', linewidth=3.0, label='Utility Max Desired Power')
    cnt += 1
    ax.set_xlim((0, 25000))
    ax.grid(True)
    ax.set_ylabel('Total Power (kW)', fontsize=20)
    ax.legend(loc='lower left', fontsize=13)
    xticks = [3560, 3560+3580, 3560+3580+3590, 3560+3580+3590+3560,
            3560+3580+3590+3560+3560, 3560+3580+3590+3560+3580,
            3560+3580+3590+3560+3580+3560]
    plt.xticks(xticks, ['', '', '', '', '', '', ''], horizontalalignment='right')
    plt.yticks(range(1000, 10000, 1000))

    row_text = [r'Avg Price ($\cent$/kWh)', 'Load Shifting (USD)', 'No Load Shifting (USD)', 'DoS Attack (USD)']
    col_text = ['6:00-7:00pm', '7:00-8:00pm', '8:00-9:00pm', '9:00-10:00pm',
            '10:00-11:00pm', '11:00-12:00am', 'Total']
    cell_data = [[3.15, 2.90, 2.75, 2.30, 1.90, 1.40, '2.40(Avg)'],
                [158.62, 130.57, 115.27, 112.65, 91.41, 57.51, 666.01],
                [217.15, 177.34, 143.98, 86.85, 55.95, 32.39, 713.66],
                [158.62, 161.85, 153.56, 114.26, 67.89, 32.39, 688.57]]
    cost_table = ax.table(cellText=cell_data, rowLabels=row_text, colLabels=col_text, rowLoc='right', loc='bottom')
    cost_table.set_fontsize(20)

    ax2 = ax.twinx()
    totals = [[666], [714], [689]]
    
    bar_width = 1180
    index = range(21450, 26000, 1180)
    bar_colors = ['red', 'blue', 'green']
    alpha=0.0
    ax2.bar(index[0], totals[0], bar_width, color=bar_colors[0], hatch=hatches[0], label='Load Shifting')
    ax2.bar(index[1], totals[1], bar_width, color=bar_colors[1], hatch=hatches[1], label='No Load Shifting')
    ax2.bar(index[2], totals[2], bar_width, color=bar_colors[2], hatch=hatches[2], label='DoS Attack')
    ax2.set_ylabel('Cost', fontsize=20)
    ax2.set_xlim([0, 25000])
    ax2.set_ylim([600, 740])
    ytick_labels = ['$600', '$620', '$640', '$660', '$680', '$700', '$720', '$740', '$760']
    ax2.set_yticks(range(600, 780, 20))
    ax2.set_yticklabels(ytick_labels)
    ax2.legend(loc='upper right', fontsize=13)
    
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(output_file, format='eps', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    cnt = 0
    ls_name = ['solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':']
    hatches = ['//', '+', 'x']
    colors_name = ['red', 'blue', 'cyan', 'peru', 'green', 'salmon', 'pink', 'lime', 'tan', 'seagreen', 'purple', 'wheat']
    output = sys.argv[1]
    plot_all(output)



