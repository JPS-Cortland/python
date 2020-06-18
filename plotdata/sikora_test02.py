# I've written lots of code in FORTRAN and C,
# but since SLAC uses Python quite a bit, I thought
# I would write a simple Python script to show that
# I can pick it up pretty quickly.
#    (Branch variation01 June 18, 2020)
# This is based on various topics in the Python tutorial:
# https://docs.python.org/3/tutorial/
#
# This script requires a datafile named tew20161214_0003.dat
# It reads in the data, finds the peaks and plots the data.
#
# Created by John Sikora: February 27, 2017
#

# import regular expressions
import re

# The file name is hard coded for this test.
# It could have been read in as a parameter.

fobj = open('tew20161214_0003.dat', 'r')

datapoints = []

# Search the data file for the string "TRACE1:"
# The spectrum data will be on the following 1000 lines.
# Strip off the comma and newline at the end of each line before converting
# the text string to a float.

for line in fobj:
    if re.findall(r'TRACE1:',line):
        print(line, end = '')
#
# the next 1000 lines contains the data points
#
        for jj in range(0,1000):
            strval = fobj.readline()
            strclean = strval.rstrip(',\n')         
            datapoints.append(float( strclean ) )
#
# Find the overall maximum value in the data set.
#
max = -200
for val in datapoints:
    if val > max:
        max = val

# Simple peak find:
# Find the peaks in the data set above a noise floor of -100 dBm
# Looks for consistent slope for +/- 2 points.
# Not the best way to do it , but it works for this data set.
#

# The related lists below should probably be combined into
# a single list (?). In C, a structure would be used.
maxlist  = []
maxindexlist = []

# Examine all of the data and at each point,
# look for a change in data values (scatter) over a short range of data points.

localmax = -200
for jj in range(5, len(datapoints) - 5 ):

    minval = 0
    maxval = -200
    for kk in range(-3,2):
        if datapoints[jj+kk] > maxval:
            maxval = datapoints[jj+kk]
        if datapoints[jj+kk] < minval:
            minval = datapoints[jj+kk]

    scatter = maxval - minval

# If the scatter in the data is larger than 5 dB, look for a peak nearby.
# For a simple test, look for a positive then negative slope -- before/after the point.
# If a maximum is found, put it in a list of maxima along with a list of indices. 

    if scatter > 5.0 and maxval >-100:            
        if (datapoints[jj]   < datapoints[jj+1]) and \
           (datapoints[jj+1] < datapoints[jj+2]) and \
           (datapoints[jj+2] > datapoints[jj+3]) and \
           (datapoints[jj+3] > datapoints[jj+4]):

           localmax = datapoints[jj+2]
           maxindex = jj+2
           maxlist.append(localmax)
           maxindexlist.append(maxindex)

           print("local maximum at ",maxindex, localmax, "with scatter", scatter)

print("max =", max)

# print(datapoints, end = ', ')

# Close the file when done.

fobj.close()


# The datapoints have been read from the file and the peaks have been found.
# Make a crude plot of the data and mark the peaks
#
# Adapted from the Canvas tutorial at  http://www.python-course.eu/tkinter_canvas.php
#
from tkinter import *

master = Tk()

canvas_width = 1000
canvas_height = 400
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

scale = -3.0
offset = 0

#
# Make a crude plot of the data, point to point.
# I'm cheating by making the width of the display window
# the same as the number of points.
# 

for jj in range(0, len(datapoints) -1 ):

    w.create_line(jj, scale*datapoints[jj]+offset, jj+1 , scale*datapoints[jj+1]+offset, fill="#476042")

# Plot the list of peaks at the peak x,y positions
# To do this, create a vertical line at the x position
# and a horizontal line at the y position of the peak.

for jj in range(0, len(maxindexlist) ):
    w.create_line(maxindexlist[jj], scale*maxlist[jj]+ offset + 10, 
                  maxindexlist[jj], scale*maxlist[jj]+ offset - 10  ,fill="#476042")

    w.create_line(maxindexlist[jj]-10, scale*maxlist[jj]+ offset, 
                  maxindexlist[jj]+10, scale*maxlist[jj]+ offset  ,fill="#476042")

mainloop()

