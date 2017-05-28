#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from importlib import import_module
import RfPredictor
# import PreProcessors.PreProcesor_01 as PreProcessor --> Esto funciona pero no es dinámico
                                                         # Forma correcta de importar paquetes en Python

PreProcessor = None

def main():

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
        print("No existe el preprocesador: '" + pre_proc + "'.")
        return 1
# -----------------------------------------------------------------------------

    print('Cargando y Preprocesando datos...')
    train, target, testIds, testVals = PreProcessor.loadData('../../DataSet/trip_train.csv',
                                                             '../../DataSet/trip_test.csv')

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
    filename = "rf_" + pre_proc + "_" + str(estimators) + ".csv"
    RfPredictor.exportResults(predictions, testIds, filename)
    return 0

main()
