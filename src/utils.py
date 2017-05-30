#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import platform


''' Carga los DataFrames de Train y Test parseando las fechas de las
    columnas de manera adecuada.
    Devuelve:
        - Tupla con los dos DataFrames. '''
def loadDataFrames(dirTrain, dirTest, dirStation, dirWeather) :

    dfTrain = pd.read_csv(dirTrain,
                          parse_dates=['start_date', 'end_date'],
                          infer_datetime_format=True)

    dfTest = pd.read_csv(dirTest,
                         parse_dates=['start_date', 'end_date'],
                         infer_datetime_format=True)
    dfWeather = pd.read_csv(dirWeather, parse_dates=['date'], infer_datetime_format=True) if dirStation != None else None
    dfStation = pd.read_csv(dirStation, parse_dates=['installation_date'], infer_datetime_format=True) if dirWeather != None else None

    return dfTrain, dfTest, dfStation, dfWeather

''' Utilizada como parámetro para función DataFrame.apply
    Para cada row, devuelve el zip code correspondiente a la ciudad.'''
def cityNameToZipCode(row) :

    if row.city == 'San Francisco' :
        return 94107

    if row.city == 'Redwood City' :
        return 94063

    if row.city == 'Palo Alto' :
        return 94301

    if row.city == 'Mountain View' :
        return 94041

    if row.city == 'San Jose' :
        return 95113

def getSystemWriteMode() :
    if platform.system() == 'Windows' :
        return 'wb'

    return 'w'
