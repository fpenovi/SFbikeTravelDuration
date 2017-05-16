import csv

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
			train.append((line[4],line[7])) #start station, end station
	with open(dirTest, 'r') as infile:
		reader = csv.reader(infile)
		next(reader, None)
		for line in reader:
			testIds.append(line[0])
			testVals.append((line[3], line[6])) #start station, end station
	return train,target,testIds, testVals