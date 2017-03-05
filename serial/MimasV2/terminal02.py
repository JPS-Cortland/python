#!/usr/bin/python3
# Original version obtained from https://github.com/StefanRvO/SerialTerminal/blob/master/terminal.py
# I've modified it since then
#

import time
from serial import Serial
import sys
from math import log
import tkinter
from tkinter import ttk
connected=0
serialport=0


def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1
def ToHexList(num):
    length=bytes_needed(num)
    if length==0:
        return 0
    liste=[]
    for i in range(length):
        bitwise=0xff<<i*8
        liste.append(chr((num & bitwise)>>8*i))
    liste.reverse()
    return liste
def ToHexList2(num):
    length=bytes_needed(num)
    if length==0:
        return 0
    liste=[]
    for i in range(length):
        bitwise=0xff<<i*8
        liste.append(hex((num & bitwise)>>8*i))
    liste.reverse()
    return liste

def ToInt(liste):
	tal=0
	for i in range(len(liste)):
		tal+=liste[i]<<((len(liste)-(i+1))*8)
	return tal


def SerialConnect():
    global serialport
    serialport = Serial(port=PortPath.get(), baudrate=19200)
    global connected
    connected=1
    print ("connected to serial port = ", serialport)
    ReceivedField.insert(tkinter.INSERT,"Connected to "+PortPath.get()+'\n')
    ReceivedField.see('end')
    

def Receive():
    reading=[]
    if connected:
        global ReceivedString
        while (serialport.inWaiting()>0):							        
            if (serialport.inWaiting() > 0):			
                reading.append(ord(serialport.read(1)))
            time.sleep(0.001)

        if reading!=[]:
            hexstring=''
            for ii in reading:
                 hexstring+=chr(ii)
            ReceivedField.insert(tkinter.INSERT,ReceivedString.get()+hexstring+'\n')
            ReceivedField.see('end')

    top.after(1,Receive)

def ListDisplay():
    global ListSelect
    if connected:
        command=str( var.get() )
        print("command = ",command)
        cmd = bytearray(command,encoding="utf-8")
        serialport.write(cmd)
        time.sleep(0.001)

    else:
         ReceivedField.insert(tkinter.INSERT,"You are not connected" + '\n')
         ReceivedField.see('end')





top=tkinter.Tk() #Main Windows

var = tkinter.StringVar()

RWidth=top.winfo_screenwidth()
RHeight=top.winfo_screenheight()
top.geometry("300x300")
top.minsize(300, 300)
top.maxsize(RWidth, RHeight)


ReceivedString=tkinter.StringVar()
PortPath=tkinter.StringVar()
ListSelect=tkinter.StringVar()

PortField=tkinter.Entry(top,textvariable=PortPath)
PortField.grid(row=90, column=0, sticky="nsew")
ConnectButton=tkinter.Button(top,command=SerialConnect,text="Connect")
ConnectButton.grid(row=90, column=1, columnspan=1, sticky="nsew")



ReceivedScrool=tkinter.Scrollbar(top)
ReceivedScrool.grid(row=600,column=500,sticky="nsew")
ReceivedField=tkinter.Text(top,bg='tan',yscrollcommand=ReceivedScrool.set)
ReceivedField.grid(row=600,columnspan=499,  sticky="nsew")


Rad1 = tkinter.Radiobutton(top, text="FIR 31", variable=var, value="fil:1", command=ListDisplay)
Rad1.grid(row=200,column=0,sticky="w")

Rad2 = tkinter.Radiobutton(top, text="Tone", variable=var, value="fil:2", command=ListDisplay)
Rad2.grid(row=210,column=0,sticky="w")

Rad3 = tkinter.Radiobutton(top, text="RingMod", variable=var, value="fil:3", command=ListDisplay)
Rad3.grid(row=220,column=0,sticky="w")

Rad3 = tkinter.Radiobutton(top, text="AutoTune", variable=var, value="fil:4", command=ListDisplay)
Rad3.grid(row=240,column=0,sticky="w")


FiltListLabel = tkinter.Label(top, text="Select Filter")
FiltListLabel.grid(row=210,column=1,sticky="ew")


filterval = tkinter.StringVar()
Filterlist = ttk.Combobox(top,textvariable=filterval, width=10)
Filterlist['values'] = ('FIR31', 'Tone', 'RingMod')
Filterlist.grid(row=220,column=1,sticky="ew")


top.columnconfigure(0, weight=1, minsize=50)      #port field
top.columnconfigure(1, weight=0, minsize=40)      #connect button
# top.columnconfigure(2, weight=1, minsize=100) 
# top.rowconfigure(100, weight=0) # not needed, this is the default behavior
top.rowconfigure(11, weight=0)
top.rowconfigure(90, weight=0)
top.rowconfigure(200, weight=0)
top.rowconfigure(210, weight=0)
top.rowconfigure(220, weight=0)
top.rowconfigure(600, weight=1) # Received Text and scrollbar
top.after(1,Receive)
top.mainloop() #Start main loop
