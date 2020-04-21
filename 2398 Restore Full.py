# IFR 2398 Calibration Dump Script
# April 2019 Colby Burkett
#
#
# This script restores all of the backed up calibration information from
# an IFR 2398 or LG SA-7270 Spectrum Analyzer
#
# Don't judge!  It's quick and dirty!
#
# Last: Use at your own risk!

from __future__ import division
import datetime
import os
import sys
import time
import visa
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H-%M-%S')
print st

# Create VISA object
rm = visa.ResourceManager()

# Open connection to UUT on GPIB ADDR 19
inst = rm.open_resource('GPIB0::7::INSTR')
inst.timeout = 10000

# Serial Number and Manufacturer Set
# MFC of 1 is IFR, MFC of 2 is LG 
#inst.write("SN MFC[1]SN[12345678]")

# Retrieve & print the ID of the UUT
uutId = inst.query("*IDN?")
print uutId

# Replace with your backup file name created by the Dump script
backupFileName='backupFileName.txt'
if (os.path.isfile(backupFileName)):
    backupFile = open(backupFileName, 'r')
else:
    print 'Backup filename invalid'

caldata = {}
d = {}
a = 0
for rowofdata in backupFile:
    caldata[a] = eval(rowofdata)
    a += 1

# RXFLAT 0-23
# IFATT 24
# RXATT 25
# SPANATT 26
# LOGTBL 27-37

# Need to set atten level to manual first
inst.write("AT MAN;")
a = 0
atten = 0
tbl=1
print "RXFLAT Restore: "+str(atten*10)+"dB",
inst.write("AT "+str(atten*10)+";")
while a < 24:
    #print a
    if tbl == 4:
        data = '<'+','.join(str(e) for e in caldata[a])+'>'
        #print tbl, atten, data
        sys.stdout.write('.')
        inst.write("RXFLAT #"+str(tbl)+" #"+str(atten)+","+data+";")
        #print("RXFLAT #"+str(tbl)+" #"+str(atten)+","+data+";")
        tbl = 1
        atten += 1
        if atten < 6:
            sys.stdout.write(str(atten*10)+"dB:")
            inst.write("AT "+str(atten*10)+";")
    else:
        data = '<'+','.join(str(e) for e in caldata[a])+'>'
        #print tbl, atten, data
        sys.stdout.write('.')
        inst.write("RXFLAT #"+str(tbl)+" #"+str(atten)+","+data+";")
        #print("RXFLAT #"+str(tbl)+" #"+str(atten)+","+data+";")
        tbl += 1
    time.sleep(0.1)
    a += 1

print "\nIFATT:",
Position = 24
entry = 0
for data in caldata[Position]:
    #print data
    sys.stdout.write('.')
    inst.write("IFATT #"+str(entry)+","+str(data)+";")
    entry += 1

print "\nRXATT:",
Position = 25
entry = 0
for data in caldata[Position]:
    #print data
    sys.stdout.write('.')
    inst.write("RXATT #"+str(entry)+","+str(data)+";")
    entry += 1

print "\nSPANATT:",
Position = 26
entry = 0
for data in caldata[Position]:
    #print data
    sys.stdout.write('.')
    inst.write("SPANATT #"+str(entry)+","+str(data)+";")
    entry += 1

print "\nLOGTBL:",
Position = 27
rbw = 0
log = 0
while Position < 38:
    sys.stdout.write("\n"+str(rbw)+":")
    for data in caldata[Position]:
        sys.stdout.write('.')
        #print "LOGTBL #"+str(rbw)+" #"+str(log)+","+str(data)+";"
        inst.write("LOGTBL #"+str(rbw)+" #"+str(log)+","+str(data)+";")
        log += 1
    rbw += 1
    Position += 1


