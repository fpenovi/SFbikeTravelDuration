#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import platform


''' Carga los DataFrames de Train y Test parseando las fechas de las
    columnas de manera adecuada.
    Devuelve:
        - Tupla con los dos DataFrames. '''
def loadDataFrames(dirTrain, dirTest) :

    dfTrain = pd.read_csv(dirTrain,
                          parse_dates=['start_date', 'end_date'],
                          infer_datetime_format=True)

    dfTest = pd.read_csv(dirTest,
                         parse_dates=['start_date', 'end_date'],
                         infer_datetime_format=True)

    return dfTrain, dfTest


def getSystemWriteMode() :
    if platform.system() == 'Windows' :
        return 'wb'

    return 'w'
