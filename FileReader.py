import os, csv
import glob
import math

def filereader(file):
    csvFile = csv.reader(file)
    csvFile.next()
    Points = []
    for line in csvFile:
        Points.append(line)
    return Points

def distance2points(x1, y1, x2, y2):
    result = math.sqrt(((x2 - x1)**2)+((y2 - y1)**2))
    return result

def totalDistance(listIn):
    count = 0
    distance = 0
    for row in listIn:
        x1 = float(listIn[count][0])
        y1 = float(listIn[count][1])
        count = count + 1
        x2 = float(listIn[count][0])
        y2 = float(listIn[count][1])
        distance = distance + distance2points(x1, y1, x2, y2)
        if(count == len(listIn) -1):
            break
    return distance


dir_path = r'C:/Users/Brandon/Downloads/drivers/drivers/1/1.csv'
#file_dir_extension = os.path.join(dir_path, '*csv')
fileIn = open(dir_path, 'r')
#for file_name in glob.glob(file_dir_extension):
#    if file_name.endswith('.csv'):
#        print file_name
#print fileIn.read(5)
filePoints = filereader(fileIn)
dist = totalDistance(filePoints)
print dist
print len(filePoints)
print dist/len(filePoints)



