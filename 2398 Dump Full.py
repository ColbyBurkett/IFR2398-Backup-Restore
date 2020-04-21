# IFR 2398 Calibration Dump Script
# April 2019 Colby Burkett
#
# This script dumps out all of the existing calibration information from
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

# Retrieve & print the ID of the UUT
# If the serial number has been corrupted, comment out the following line and
# uncomment the one after it
uutId = inst.query("*IDN?")
#uutId = "Junk"
print uutId

# Open file to write the calibration data to
# Check to make sure the backup file doesn't exit
# so it isn't overwritten
# If the serial number has been corrupted, comment out the following line and
# uncomment the one after it
backupFileName='backupData_'.strip()+uutId.split(',')[1].strip()+'_'+uutId.split(',')[2].strip()+'_'+st+'.txt'
#backupFileName='backupData_'+st+'.txt'

if (not os.path.isfile(backupFileName)):
    backupFile = open(backupFileName, 'w')
else:
    print 'Backup file exists.  Please move it and retry.'
    sys.exit(1)

# Log the UUT serial # to the file
#backupFile.write('*** Data pulled from UUT: ' + uutId + '\n')

# "RXFLAT {Table#}" Returns all of the entries for table # and current Atten value (Change atten value and repull tables 1-4)
atten = 0
inst.write("AT MAN;")
sys.stdout.write("Backing up RXFLAT Data for Atten Lvl: ")
while atten < 60:
    sys.stdout.write(str(atten)+"dB")
    inst.write("AT "+str(atten)+";")
    #backupFile.write('RXFLAT '+str(atten)+'dB\r\n')
    table = 1
    while table < 5:
        data = inst.query("RXFLAT "+str(table)+"?")
        #print atten,table,data
        #backupFile.write(str(table)+': '+data)
        backupFile.write(data)
        table += 1
    atten += 10
    if atten < 60:
        sys.stdout.write(',')
sys.stdout.write('\n')

# IFATT data
#backupFile.write('IFATT\r\n')
sys.stdout.write('Backing up IFATT Data')
backupFile.write('[',)
i = 0
while i < 7:
    data = float(inst.query("IFATT "+str(i)+"?"))
    if i != 6:
        #print("%.2f" % data)+',',
        sys.stdout.write('.')
        backupFile.write(str("%.2f" % data)+',',)
    else:
        #print("%.2f" % data)+']'
        sys.stdout.write('.\n')
        backupFile.write(str("%.2f" % data)+']\n')
    i += 1

# RXATT data
#backupFile.write('RXATT\r\n')
sys.stdout.write('Backing up RXATT Data')
backupFile.write('[',)
i = 0
while i < 6:
    #data = inst.query("RXATT "+str(i)+"?")
    data = float(inst.query("RXATT "+str(i)+"?"))
    if i != 5:
        sys.stdout.write('.')
        backupFile.write(str("%.2f" % data)+',',)
    else:
        sys.stdout.write('.\n')
        backupFile.write(str("%.2f" % data)+']\n')
    i += 1

# SPANATT data
#backupFile.write('SPANATT\r\n')
sys.stdout.write('Backing up SPANATT Data')
backupFile.write('[',)
i = 0
while i < 11:
    #data = inst.query("SPANATT "+str(i)+"?")
    data = float(inst.query("SPANATT "+str(i)+"?"))
    if i != 10:
        sys.stdout.write('.')
        backupFile.write(str("%.2f" % data)+',',)
    else:
        sys.stdout.write('.\n')
        backupFile.write(str("%.2f" % data)+']\n')
    i += 1

# "LOGTBL #0 #0?;" Returns all of the entries for Log table # for RBW #
# LOGTBL #RBW #dB
sys.stdout.write('Backing up LOGTBL Data')
rbw = 0
while rbw < 11:
    log = 0
    #backupFile.write('LOG: '+str(rbw)+'\r\n')
    backupFile.write('[',)
    while log < 9:
        data = float(inst.query("LOGTBL #"+str(rbw)+" #"+str(log)+"?;"))
        if log != 8:
            sys.stdout.write('.')
            backupFile.write(str("%.2f" % data)+',',)
        else:
            backupFile.write(str("%.2f" % data)+']\n')
        log += 1
    rbw += 1

print ''

# Cal Signal Level
# Not used in backup right now
#data = inst.query("LEVCAL ?")
#print "LEVCAL:",data
#backupFile.write("Cal Signal Level: "+data)

backupFile.close()
