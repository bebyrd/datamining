__author__ = 'bebyrd'
import numpy
import sys
import os
import glob
import re
import csv
import random


from subprocess import *



def fileRead(driver_pathname):
    regex = re.compile(r'')
    count = 0
    drivers = sorted(glob.glob(driver_pathname+'/*'))
    print drivers


def main(argv=None):
    #main code; ran if opened by itself
    if argv is None:
        argv = sys.argv
    driver_pathname = argv[1] #folder containing all the driver csv files
    assert os.path.exists(driver_pathname)

    #call fileRead






if __name__ == "__main__": sys.exit(main())


