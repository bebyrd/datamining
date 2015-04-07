__author__ = 'bebyrd'
import sys
import os
import glob
import re
import csv

from subprocess import *

#if len(sys.argv) < 1:
#    print('Usage: {0} tripInput'.format(sys.argv[0]))
#    raise SystemExit

fileReader1 = 'FileReader1.py'
assert os.path.exists(fileReader1),'FileReader1.py not found'

trip_pathname = sys.argv[1]
assert os.path.exists(trip_pathname)

#trip_pathname = '/Users/bebyrd/Documents/gsu/drivers/15'
#print trip_pathname

drivers = glob.glob(trip_pathname+'/*')
print drivers
for driver in drivers:
    regex = re.compile(r'drivers\d+')
    regex2 = re.compile(r'\d+')
    driverNum = regex2.search(driver).group(0)
    trips = glob.glob(driver+'/*')
    #print trips


    print driverNum
    f = open(driverNum+'.csv','w')
    for trip in trips:
        #print trip
        cmd = 'python %s %s' % (fileReader1,trip)
        output = Popen(cmd, shell=True, stdout=PIPE).communicate()
        #print output
        f.write(output[0])
    f.close()
