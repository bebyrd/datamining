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

#trip_pathname = sys.argv[1]
#assert os.path.exists(trip_pathname)

trip_pathname = '/Users/bebyrd/Documents/gsu/drivers/15'
#print trip_pathname

#drivers = glob.glob(trip_pathname+'/*')
#print drivers


trips = glob.glob(trip_pathname+'/*')
#print trips

regex = re.compile(r'drivers\d+')
regex2 = re.compile(r'\d+')
outnum = regex2.search(trip_pathname).group(0)
print outnum
f = open(outnum+'.csv','w')
for trip in trips:
    print trip
    cmd = 'python %s %s' % (fileReader1,trip)
    output = Popen(cmd, shell=True, stdout=PIPE).communicate()
    print output
    #f.write(output+'\n')
f.close()
