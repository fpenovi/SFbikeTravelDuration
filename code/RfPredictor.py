from sklearn.ensemble import RandomForestRegressor
import csv

def predict(train, target, testIds, testVals):
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