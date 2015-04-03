import os, csv
import glob
import math

#process the csv file with x and y coordinates
def filereader(file):
    csvFile = csv.reader(file)
    #bypass the first line which just states x and y
    csvFile.next()
    Points = []
    for line in csvFile:
        Points.append(line)
    return Points

#compute distance of 2 points
def distance2points(x1, y1, x2, y2):
    result = math.sqrt(((x2 - x1)**2)+((y2 - y1)**2))
    return result


#used to find the average acceleration over the seconds after a stop
def goAnalysis(listIn, location):
    global totalStopAccelerations
    count = 0
    if len(listIn) < location + 10:
        return
    for x in listIn:
        x1 = float(listIn[location + count][0])
        y1 = float(listIn[location + count][1])
        x2 = float(listIn[location + count + 1][0])
        y2 = float(listIn[location + count + 1][1])

        currentDistance = distance2points(x1, y1, x2, y2)

        x1 = x2
        y1 = y2

        count = count + 1

        x2 = float(listIn[location + count + 1][0])
        y2 = float(listIn[location + count + 1][1])
        nextDistance = distance2points(x1, y1, x2, y2)
        workingDistance = nextDistance - currentDistance
        #test if acceleration is over
        if 4.0 > workingDistance or count == 9:
            break
    leavingSpeed = nextDistance/(count)
    #leavingSpeed = distance2points(listIn[location+10][0], listIn[location+10][1], listIn[location + 9][0], listIn[location + 9][1])/9
    totalStopAccelerations = totalStopAccelerations + leavingSpeed

#used to find the average deceleration over the seconds up to a stop
def stopAnalysis(listIn, location):
    global totalStops, totalStopDecelerations
    count = 0
    if 0 > location - 10:
        return
    for x in listIn:

        #get the x and y coordinates of 2 points
        x1 = float(listIn[location - count][0])
        y1 = float(listIn[location - count][1])
        x2 = float(listIn[location - count - 1][0])
        y2 = float(listIn[location - count - 1][1])

        currentDistance = distance2points(x1, y1, x2, y2)
        #set the next x y to the last x2 y2
        x1 = x2
        y1 = y2

        count = count + 1
        #go back one more coordinate
        x2 = float(listIn[location - count - 1][0])
        y2 = float(listIn[location - count - 1][1])
        previousDistance = distance2points(x1, y1, x2, y2)
        workingDistance = currentDistance - previousDistance
        #test if acceleration is over
        if -4.0 > workingDistance or count == 9:
            break
    initialSpeed = -previousDistance/(count)
    #x1 = float(listIn[location - 10][0])
    #y1 = float(listIn[location - 10][1])
    #x2 = float(listIn[location - 9][0])
    #y2 = float(listIn[location - 9][1])
    #initialSpeed = distance2points(x1, y1, x2, y2)/9
    totalStopDecelerations = totalStopDecelerations + initialSpeed
    totalStops = totalStops + 1

def totalDistance(listIn):
    global max_velocity, max_acceleration, max_deceleration
    nextDistance = -999.0
    count = 0
    distance = 0.0
    tripPoints = listIn
    currentDistance = 0.0
    isStopped = False
    for row in listIn:
        #first coordinate
        x1 = float(listIn[count][0])
        y1 = float(listIn[count][1])
        count = count + 1
        #next coordinate
        x2 = float(listIn[count][0])
        y2 = float(listIn[count][1])

        if nextDistance != currentDistance:
            nextDistance = currentDistance
        #calculate distance which is velocity in m/s
        currentDistance = distance2points(x1, y1, x2, y2)

        #compute the change in speed from one coordinate to the next
        changeSpeed = nextDistance - currentDistance
        #check for max acceleration
        if max_acceleration < changeSpeed:
            max_acceleration = changeSpeed
        #check for max deceleration
        if max_deceleration > changeSpeed:
            max_deceleration = changeSpeed

        #compute total distance
        distance = distance + currentDistance

        #determine if the driver has stopped or is not moving much
        if currentDistance < 1 and isStopped == False:
            stopAnalysis(tripPoints, count)
            isStopped = True
        #determine if the driver has started moving again into a stop
        if currentDistance >= 1 and isStopped == True:
            goAnalysis(tripPoints, count)
            isStopped = False
        #determine maximum speed
        if max_velocity < currentDistance:
            max_velocity = currentDistance

        #make sure we do not go over the list length and because we go one over to calculate distance subtract 1
        if(count == len(listIn) -1):
            break
    return distance

#Brandon Working Directory
dir_path = r'C:/Users/Brandon/Downloads/drivers/drivers/1/5.csv'

        #file_dir_extension = os.path.join(dir_path, '*csv')

#Open the File and create a file object
fileIn = open(dir_path, 'r')

        #for file_name in glob.glob(file_dir_extension):
        #    if file_name.endswith('.csv'):
        #        print file_name
        #print fileIn.read(5)


#variables declared so they can be used globally
totalStops = 0
totalStopAccelerations = 0.0
totalStopDecelerations = 0.0
max_velocity = 0.0
max_acceleration = 0.0
max_deceleration = 0.0

filePoints = filereader(fileIn)
dist = totalDistance(filePoints)

#print results
print 'Total Stops = %d' % totalStops
print 'Average Stop Deceleration = %f m/s2' % (totalStopDecelerations/totalStops)
print 'Average Stop Acceleration = %f m/s2' % (totalStopAccelerations/totalStops)
print 'Total Trip Distance = %.3f meters' % dist
print 'Total Seconds = %d seconds' % len(filePoints)
print 'Average Velocity = %f m/s' % (dist/len(filePoints))
print 'Max Velocity = %f m/s' % max_velocity
print 'Max Acceleration = %f m/s2' % max_acceleration
print 'Max Deceleration = %f m/s2' % max_deceleration



