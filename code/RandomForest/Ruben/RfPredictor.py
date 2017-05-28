from sklearn.ensemble import RandomForestRegressor
import csv


def predict(train, target, testIds, testVals):

	rf = RandomForestRegressor(n_estimators=100, n_jobs=-1) 	# Jobs = -1 elije numero de
	print("Volcando puntos...")									# jobs segun cantidad de cores.
	rf.fit(train, target)
	print("Prediciendo...")
	predictions = rf.predict(testVals)

	with open("rf_sum_svd_100.csv", "w") as outfile:
		rows = [["Prediction", "Id"]]

		for prediction, idTest in zip(predictions, testIds):
			rows.append([prediction, idTest])

		out_csv = csv.writer(outfile)
		out_csv.writerows(rows)
