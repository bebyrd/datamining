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

    count = 0
    print driver_pathname
    drivers = sorted(glob.glob(driver_pathname+'/*'))
    return drivers

def randomDriver(drivers):
    return random.randint(0,len(drivers))

def main(argv=None):
    fDriver = -1
    #main code; ran if opened by itself
    if argv is None:
        argv = sys.argv
    driver_pathname = argv[1] #folder containing all the driver csv files
    assert os.path.exists(driver_pathname)

    #call fileRead
    drivers = fileRead(driver_pathname)
    trueDriver = randomDriver(drivers)

    print "true driver: " + drivers[trueDriver]
    test = True

    while test:
        fDriver = randomDriver(drivers)
        print "first random: " + drivers[fDriver]
        if not fDriver == trueDriver:
            test = False



if __name__ == "__main__": sys.exit(main())


