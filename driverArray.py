__author__ = 'bebyrd'
import numpy
import sys
import os
import glob
import re
import csv
import random
import sklearn


from subprocess import *




def fileRead(driver_pathname):

    count = 0
    print driver_pathname
    drivers = sorted(glob.glob(driver_pathname+'/*'))
    return drivers

def randomDriver(drivers):
    return random.randint(0,len(drivers))

def driverToNumpy(input_csv):
    dataset = numpy.genfromtxt(open(input_csv,'r'), delimiter=',', usecols=(2, 3, 6, 7, 8, 9, 10, 11, 12, 13))
    return sklearn.preprocessing.scale(dataset)


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
    print trueDriver
    print "true driver: " + drivers[trueDriver]
    test = True

    while test:

        fDriver = randomDriver(drivers)
        print fDriver
        print "first random: " + drivers[fDriver]
        if not fDriver == trueDriver:
            test = False

    dataset = driverToNumpy(drivers[trueDriver])

    print dataset



if __name__ == "__main__": sys.exit(main())


