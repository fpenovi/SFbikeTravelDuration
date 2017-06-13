#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from importlib import import_module
from sklearn.preprocessing import StandardScaler
import RfPredictor
import src.validator as Validator
import src.utils as utils
PreProcessor = None

def main():

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if (len(sys.argv) < 3) :
        print("Modo de uso -> python main.py <n_estimators> <pre_procesing_module>")
        return 0

    estimators = sys.argv[1]
    pre_proc = sys.argv[2]

# ----------------------------VALIDO ARGUMENTOS CLI----------------------------
    try:
        estimators = int(estimators)
    except ValueError as e:
        print("Error: parámetro n_estimators debe ser un número.")
        return 1

    if (not pre_proc.isdigit() or len(pre_proc) < 2) :
        print("Error: parámetro pre_procesing_module debe ser numérico y de dos caracteres (i.e: '01').")
        return 1

    try:
        PreProcessor = import_module('PreProcessors.PreProcesor_' + pre_proc)
    except ImportError as e:
        print("Error importando el preprocesador: '" + pre_proc + "'.")
        print "Error:", e
        return 1
# -----------------------------------------------------------------------------
    start = time.time()     # Arranco a contar el tiempo
    print('Cargando y Preprocesando datos...')
    train, target, testIds, testVals = PreProcessor.loadData('../../DataSet/trip_train.csv',
                                                             '../../DataSet/trip_test.csv',
                                                             '../../DataSet/station.csv',
                                                             '../../DataSet/weather.csv')

    print 'Estandarizando data sets...'
    scaler = StandardScaler().fit(train)
    train = scaler.transform(train)
    testVals = scaler.transform(testVals)

    predictions = RfPredictor.predict(train, target, testIds, testVals, estimators)

    # Permito que python libere la memoria
    train = None
    target = None
    testVals = None

    print 'Calculando score...'
    print 'Score:', Validator.getOutputScore(testIds, predictions)

    # Archivo: <algoritmo>_<pre_processor>_<estimators>.csv || ejemplo: rf_01_200.csv
    filename = "rf_" + pre_proc + "_" + str(estimators) + ".csv"
    utils.exportResults(predictions, testIds, filename)

    end = time.time()
    m, s = divmod(end - start, 60)
    h, m = divmod(m, 60)
    print 'Tiempo:', "%02d:%02d:%02d" % (h, m, s)
    return 0

main()
