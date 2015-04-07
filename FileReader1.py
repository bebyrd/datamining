import os, csv
import glob
import math
import sys

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

def angularVelocity(x1,y1,x2,y2):
    dir1 = math.atan2(x1,y1)
    dir2 = math.atan2(x2,y2)
    dx = x2-x1
    dy = y2-y1
    bearing = (180/math.pi) * math.atan2(dy, dx)
    return bearing

def totalDistance(listIn):
    global max_velocity, max_acceleration, max_deceleration, max_angularAccel, totalDirChange, negAngleCount, posAngleCount
    global min_angularAccel,max_angularVelocity,min_angularVelocity, avgNeg_angularVelocity, avgPos_angularVelocity
    nextDistance = -999.0
    count = 0
    distance = 0.0
    tripPoints = listIn
    currentDistance = 0.0
    isStopped = False
    posAngleCount = 0
    negAngleCount = 0
    lastHeading = 1000
    angleChange = 0
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
        #calculate current heading
        if x1 != x2 and y1 != y2:
            heading = angularVelocity(x1,y1,x2,y2)
            if lastHeading == 1000:
                #ignore the first one!
                lastHeading = heading
            else:
                #print headings and change in headings
                angleChange = heading - lastHeading
                #print 'last heading: %d, new heading: %d, angleChg: %d' %(lastHeading,heading,angleChange)
            #print 'x1:%d y1:%d x2:%d y2:%d ' % (x1,y1,x2,y2)
            if angleChange < 0:
                negAngleCount = negAngleCount+1
                avgNeg_angularVelocity = avgNeg_angularVelocity + angleChange
            if angleChange > 0:
                posAngleCount = posAngleCount+1
                avgPos_angularVelocity = avgPos_angularVelocity + angleChange
            totalDirChange = negAngleCount + posAngleCount
            lastHeading = heading
            #check for max Angular Velocity
            if max_angularVelocity < angleChange:
                max_angularVelocity = angleChange
            #check for min Angular Velocity
            if min_angularVelocity > angleChange:
                min_angularVelocity = angleChange
            #print 'angle count: %d, avg angle change: %f '% (angleCount, (avg_angularVelocity/angleCount))

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
#Ben Working Directory (comment out when not used!)
dir_path = '/Users/bebyrd/Documents/gsu/drivers/1/5.csv'

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
totalDirChange = 0
negAngleCount = 0
posAngleCount = 0
max_velocity = 0.0
max_acceleration = 0.0
max_deceleration = 0.0
max_angularVelocity = 0.0
min_angularVelocity = 0.0
max_angularAccel = 0.0
min_angularAccel = 0.0
avgNeg_angularVelocity = 0.0
avgPos_angularVelocity = 0.0

filePoints = filereader(fileIn)
dist = totalDistance(filePoints)

#print results
#print 'Total Stops = %d' % totalStops
#print 'Average Stop Deceleration = %f m/s2' % (totalStopDecelerations/totalStops)
#print 'Average Stop Acceleration = %f m/s2' % (totalStopAccelerations/totalStops)
#print 'Total Trip Distance = %.3f meters' % dist
#print 'Total Seconds = %d seconds' % len(filePoints)
#print 'Average Velocity = %f m/s' % (dist/len(filePoints))
#print 'Max Velocity = %f m/s' % max_velocity
#print 'Max Acceleration = %f m/s2' % max_acceleration
#print 'Max Deceleration = %f m/s2' % max_deceleration
#print 'Max Angular Velocity = %f deg/s' % max_angularVelocity
#print 'Min Angular Velocity = %f deg/s' % min_angularVelocity
#print 'Neg Avg Angular Velocity = %f deg/s' % (avgNeg_angularVelocity/negAngleCount)
#print 'Pos Avg Angular Velocity = %f deg/s' % (avgPos_angularVelocity/posAngleCount)

#print csv format
print '%d, %f, %f, %.3f, %d, %f, %f, %f, %f, %f, %f, %f, %f' % (totalStops, (totalStopDecelerations/totalStops), (totalStopAccelerations/totalStops),dist, len(filePoints), (dist/len(filePoints)), max_velocity, max_acceleration, max_deceleration, max_angularVelocity, min_angularVelocity, (avgNeg_angularVelocity/negAngleCount),(avgPos_angularVelocity/posAngleCount))


