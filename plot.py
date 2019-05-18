## Import modules
import matplotlib, sys, datetime, time
matplotlib.use('TkAgg')
from math import *
from numpy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import dates
import matplotlib.pyplot as plt
from Tkinter import *

## Load the data
data = loadtxt("data/data011c.txt", unpack = True, skiprows=1, comments = '#')
temperature = data[7]
humidity = data[6]
light = data[8]
timer = data[9]
year, month, day, hour, minute, second = data[0], data[1], data[2], data[3], data[4], data[5]

## Make empty are to append the formatted dates
date_times = [] 

## Format the dates to dd.mm.yyyy hh:mm:ss
for i in range(len(year)):  # can be the length of any arbitrary data set
    # this makes a nice long string of the "day.month.year hour:min:sec"
    date_times.append(str(int(day[i])).zfill(2) + "." + str(int(month[i])).zfill(2) + "." + str(int(year[i])) +
                 " " + str(int(hour[i])).zfill(2) + ":" + str(int(minute[i])).zfill(2) + ":" + str(int(second[i])).zfill(2) )

## String format of the date
pattern = '%d.%m.%Y %H:%M:%S'

## Convert the list of date_times to epoch time in seconds
epoch = []
for datetimes in date_times:
    epoch.append(int(time.mktime(time.strptime(datetimes, pattern))))

## Convert epoch time to list of dateformatter objects
dts = map(datetime.datetime.fromtimestamp, epoch)
fds = dates.date2num(dts)
hfmt = dates.DateFormatter('%m/%d %H:%M')

## Create interface object
master = Tk()
## Set the title and size
master.title("Room Sensor")
master.geometry("1200x600")

## Create figure to add onto interface window
f = Figure(figsize=(9,5), dpi=100,)# facecolor='black')
## Not sure what zorder does
f.zorder
## within the figure create subplot called a
a = f.add_subplot(111)

## Add figure onto interface window
dataPlot = FigureCanvasTkAgg(f, master)
dataPlot.draw()
## Turn figure into a widget
dataPlot.get_tk_widget().place(x = 240, y = 40)
## Add plot toolbar widget
toolbar = NavigationToolbar2TkAgg(dataPlot, master)
toolbar.update()
toolbar.place(x = 240, y = 560)

## Functions to switch between plots        

def show_temp():
    ## Clear the figure
    a.clear()
    ## Plot the temperature
##    a.plot(timer,temperature, "r.--")
    a.plot(fds,temperature, "r.--")
    a.set_ylabel("Temperature (Degrees Celsius)", color = "r")
    a.xaxis.set_major_formatter(hfmt)
    a.grid(color = "r")
##    a.set_ylim([20.0,30.0])
    for tick in a.xaxis.get_major_ticks():
        tick.label.set_fontsize(7) 
        tick.label.set_rotation(15)
        tick.label.set_color("r")
    for tick in a.yaxis.get_major_ticks():
        tick.label.set_color("r")
    ## Reset the toolbar
    toolbar.update()
    f.canvas.draw()
    
def show_humidity():
    a.clear()
    a.plot(fds,humidity, "b.--")
    a.set_ylabel("Humidity %", color = "b")
    a.xaxis.set_major_formatter(hfmt)
    a.grid(color = "blue")
    for tick in a.xaxis.get_major_ticks():
        tick.label.set_fontsize(7) 
        tick.label.set_rotation(15)
        tick.label.set_color("b")
    for tick in a.yaxis.get_major_ticks():
        tick.label.set_color("b")
    toolbar.update()
    f.canvas.draw()
    
def show_light():
    a.clear()
    a.plot(fds,light, "g.--")
    a.set_ylabel("Ambient Light", color = "g")
    a.xaxis.set_major_formatter(hfmt)
    a.grid(color = "g")
    for tick in a.xaxis.get_major_ticks():
        tick.label.set_fontsize(7) 
        tick.label.set_rotation(15)
        tick.label.set_color("g")
    for tick in a.yaxis.get_major_ticks():
        tick.label.set_color("g")
    toolbar.update()
    f.canvas.draw()

## Load icon and button images
tempButton = PhotoImage(file="images/temp_button.gif")
hmdButton = PhotoImage(file="images/hmd_button.gif")
lightButton = PhotoImage(file="images/light_button.gif")
tempIcon = PhotoImage(file="images/temp_icon.gif")
hmdIcon = PhotoImage(file="images/hmd_icon.gif")
lightIcon = PhotoImage(file="images/light_icon.gif")

## Create button widgets
Button1 = Button(master, image = tempButton, command = show_temp, height = 50, width = 109)
Button2 = Button(master, image = hmdButton, command = show_humidity, height = 50, width = 109)
Button3 = Button(master, image = lightButton, command = show_light, height = 50, width = 109)
## Create labels
Label1 = Label(master, image = tempIcon, height = 50, width = 50)
Label2 = Label(master, image = hmdIcon, height = 50, width = 50)
Label3 = Label(master, image = lightIcon, height = 50, width = 50)
## Place the buttons and labels to specific location
Button1.place(x=60,y=110)
Button2.place(x=60,y=260)
Button3.place(x=60,y=410)
Label1.place(x=180, y=111)
Label2.place(x=180, y=261)
Label3.place(x=180, y=411)
## Start with the temperature graph showing
show_temp()
## Run the main interface loop
master.mainloop()
