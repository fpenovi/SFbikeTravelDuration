#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestRegressor
import csv


def predict(train, target, testIds, testVals, estimators):

    rf = RandomForestRegressor(n_estimators=estimators, n_jobs=-1) 	# Jobs = -1 elije numero de
                                                                    # jobs segun cantidad de cores.
    print("Volcando puntos...")
    rf.fit(train, target)

    print("Prediciendo...")
    predictions = rf.predict(testVals)

    return predictions

def exportResults(predictions, testIds, filename) :

    print("Guardando a archivo...")

    with open(filename, "w") as outfile:
        rows = [["id", "prediction"]]

        for idTest, prediction in zip(testIds, predictions):
            rows.append([idTest, prediction])

        out_csv = csv.writer(outfile)
        out_csv.writerows(rows)

    print("Se guardó a " + filename + " exitosamente")
