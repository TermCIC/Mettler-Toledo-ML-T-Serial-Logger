import serial
import time as t
import list_ports
import tkinter
from datetime import datetime
import os
import csv
import re

count = 1
seq = 0
save = list(range(1, 60))

print("This is TermCIC's datalogger for ML-T Precision Balances and Scales (Mettler Toledo).")
print("Why making this program? Simple, the software provided by Mettler Toledo doesn't make sense.")

# Setting serial port
print("Detecting serial ports...")
t.sleep(1)
ports = list_ports.comports()
for p in ports:
    print(p.device)
print(len(ports), 'ports found')
portName = input("Select a serial port (e.g. type COM3): ")
print("Connecting to {}...".format(portName))
t.sleep(1)
ser = serial.Serial('{}'.format(portName), baudrate=9600, timeout=1)
currentData = ser.readline()
print("The current read from ML-T is {}".format(currentData))
print()

# Select path to save data
print("Detecting current directory...")
t.sleep(1)
root = tkinter.Tk()
root.withdraw() #use to hide tkinter window
currdir = os.getcwd()
print("The current directory is: {}".format(currdir))
fileName = input("Input a filename to log data: ")
path = "{}\{}.csv".format(currdir,fileName)
print(path)
print("Data save to: {}".format(path))
print()

# Get time
print("Setting time...")
t.sleep(1)
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
hour = now.strftime("%H")
minute = now.strftime("%M")
second = now.strftime("%S")
print("The current time is: {}/{}/{}/{}/{}/{}".format(year, month, day, hour, minute, second))
print("Creating csv file...")
with open(path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Year", "Month", "Day", "Hour", "Minute", "Count (min.)", "Weight (mg)"])
print("Done!")
print()


while True:
    ser.reset_input_buffer()
    point = re.findall("\d+\.\d+", str(ser.readline()))
    ca = divmod(count, 60)
    ca = ca[1]-1
    save[ca] = point
    print(save)
    print(ca)
    if ca == -1:
        read = max(save)
        if len(read) == 0:
            print("Read value invalid")
            read = "NA"
        else:
            read = float(read[0])*1000
            print("The maximum value in 60 points is: {}".format(read))
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")
        print("Writing to csv...")
        with open(path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([year, month, day, hour, minute, seq, read])
            print("Done!")
    count = count + 1
    seq = seq + 0.0174418604651167
    t.sleep(1)
