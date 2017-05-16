import csv
from sklearn.ensemble import RandomForestRegressor

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

def classify(train, target, testIds, testVals):
	#Como tengo un celeron asqueroso en primera instancia se prueba con n_jobs=1
	rf = RandomForestRegressor(n_estimators=100, n_jobs=1) 
	print("Volcando puntos...")
	rf.fit(train, target)
	print("Prediciendo...")
	predictions = rf.predict(testVals)
	with open("rf_sum_svd_100.csv", "w") as outfile:
		rows = [["Prediction", "Id"]]
		for prediction, idTest in zip(predictions, testIds):
			rows.append([prediction, idTest])
		out_csv = csv.writer(outfile)
		out_csv.writerows(rows)

def doPrediction():
	train,target,testIds, testVals = loadData('../DataSet/trip_train.csv', '../DataSet/trip_test.csv')
	classify(train, target, testIds, testVals)