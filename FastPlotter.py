"""
FastPlotter.py
This is a simple python script for quickly plotting
the arduino data.
by: John Feng
"""

from pylab import *
import numpy as np
import matplotlib.cm as cm

datafile = "MP037.txt"  # name of datafile you're plotting
y_labels = ("temp (C)", "humidity (%)")     # array of xlabel strings
x_labels = ("hours", "hours")       # same for ylabel
titlename = "Start time: 19:17 Friday"  #plot title, never used =/

data = np.loadtxt(datafile, comments= "#")  
startrow = 8940
data = data[startrow:, :]
hours = data[:,0]/60.0
halfdays = np.arange(0, max(hours), 12)  # number of 12 hour points to plot vertical lines

number_of_plots = shape(data)[1] -1

# for info on color maps, search: "matplotlib colormaps"
colors = cm.gist_rainbow(np.linspace(0, 1, number_of_plots))

for i in range(number_of_plots):
    subplot(number_of_plots, 1, i+1)
    plot(hours ,data[:,i+1] ,color = colors[i], marker='.')
    for k in range(len(halfdays)):
        axvline(x=halfdays[k], ymin=0, ymax =100, linewidth=0.2, color='k')

    # plot labels    
    xlabel(x_labels[i])
    ylabel(y_labels[i])
    if i ==0:
        title(titlename)
show()
    
