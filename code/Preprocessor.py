import csv
from numpy import array
from dateutil.parser import parse as parseDate

#Constants subscription type
SUBSCRIBER = 0
CUSTOMER = 1


def loadData(dirTrain, dirTest):
	target = []
	train = []
	testIds = []
	testVals = []
	with open(dirTrain, 'r') as infile:
		reader = csv.reader(infile)
		next(reader, None)
		for line in reader:
			target.append(float(line[1]))
			train.append(parseLineDataTrain(line))
	with open(dirTest, 'r') as infile:
		reader = csv.reader(infile)
		next(reader, None)
		for line in reader:
			testIds.append(line[0])
			testVals.append(parseLineDataTest(line))
	return train,target,testIds, testVals

def parseLineDataTrain(line):
	startDate = parseDate(line[2])
	endDate = parseDate(line[5])
	startStation = line[4]
	endStation = line[7]
	subscriptionType = line[9]
	return getDataArray(startDate, endDate, startStation, endStation, subscriptionType)

def parseLineDataTest(line):
	startDate = parseDate(line[1])
	endDate = parseDate(line[4])
	startStation = line[3]
	endStation = line[6]
	subscriptionType = line[8]
	return getDataArray(startDate, endDate, startStation, endStation, subscriptionType)	

def getDataArray(startDate, endDate, startStation, endStation, subscriptionType):
	return array(getDateInfo(startDate) + getDateInfo(endDate) + [startStation, endStation, SUBSCRIBER if subscriptionType == 'Subscriber' else CUSTOMER])

def getDateInfo(aDatetime):
	return [aDatetime.year, aDatetime.timetuple().tm_yday, aDatetime.weekday(), aDatetime.hour + (float(aDatetime.minute)/60)]