__author__ = 'bebyrd'
import sys
import os
from subprocess import *

if len(sys.argv) < 1:
    print('Usage: {0} tripInput'.format(sys.argv[0]))
    raise SystemExit

fileReader1 = './FileReader1.py'
assert os.path.exists(fileReader1),'FileReader1.py not found'

trip_pathname = sys.argv[1]
assert os.path.exists(trip_pathname)

print trip_pathname