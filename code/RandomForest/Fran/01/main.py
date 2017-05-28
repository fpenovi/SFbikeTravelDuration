#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import PreProcessor
import RfPredictor

def main():

    if (len(sys.argv) < 2) :
        print("Modo de uso -> python main.py <n_estimators>")
        return 0

    estimators = sys.argv[1]

    try:
        estimators = int(estimators)
    except ValueError as e:
        print("Error: parámetro n_estimators debe ser un número.")
        return 1

    print('Cargando y Preprocesando datos...')
    train, target, testIds, testVals = PreProcessor.loadData('../../../../DataSet/trip_train.csv',
                                                             '../../../../DataSet/trip_test.csv')

    predictions = RfPredictor.predict(train, target, testIds, testVals, estimators)

    # Permito que python libere la memoria
    train = None
    target = None
    testVals = None

    filename = "rf_" + str(estimators) + ".csv"
    RfPredictor.exportResults(predictions, testIds, filename)
    return 0

main()
