#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from importlib import import_module
import RidgePredictor
import src.validator as Validator
PreProcessor = None

def main():

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if (len(sys.argv) < 2) :
        print("Modo de uso -> python main.py <pre_procesing_module>")
        return 0

    pre_proc = sys.argv[1]

# ----------------------------VALIDO ARGUMENTOS CLI----------------------------

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

    predictions = RidgePredictor.predict(train, target, testIds, testVals)

    # Permito que python libere la memoria
    train = None
    target = None
    testVals = None

    print 'Calculando score...'
    print 'Score:', Validator.getOutputScore(testIds, predictions)

    # Archivo: <algoritmo>_<pre_processor>.csv || ejemplo: ridge_02.csv
    filename = "ridge_" + pre_proc + ".csv"
    RidgePredictor.exportResults(predictions, testIds, filename)

    end = time.time()
    m, s = divmod(end - start, 60)
    h, m = divmod(m, 60)
    print 'Tiempo:', "%02d:%02d:%02d" % (h, m, s)

    return 0

main()
