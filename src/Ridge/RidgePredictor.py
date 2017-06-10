#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.linear_model import Ridge
import csv
import sys
import src.utils as utils

def predict(train, target, testIds, testVals):

    ridge = Ridge()
    print("Volcando puntos...")
    ridge.fit(train, target)

    print("Prediciendo...")
    predictions = ridge.predict(testVals)

    return predictions

def exportResults(predictions, testIds, filename) :

    print("Guardando a archivo...")

    with open(filename, utils.getSystemWriteMode()) as outfile:
        rows = [["id", "duration"]]

        for idTest, prediction in zip(testIds, predictions):
            rows.append([idTest, prediction])

        out_csv = csv.writer(outfile)
        out_csv.writerows(rows)

    print("Se guardó a " + filename + " exitosamente")