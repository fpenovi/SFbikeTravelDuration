#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os.path import dirname, abspath
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

    # numero de preprocessor:
    # Carpeta padre que contiene el codigo. Para llevar tracking de
    # con que features se realizó la submission.

    # Archivo: <algoritmo>_<pre_processor>_<estimators>.csv
    # ejemplo: rf_01_200.csv
    pre_processorNumber = dirname(abspath(__file__)).split('/')[-1]
    filename = "rf_" + pre_processorNumber + "_" + str(estimators) + ".csv"
    RfPredictor.exportResults(predictions, testIds, filename)
    return 0

main()
