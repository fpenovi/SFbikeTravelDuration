#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import platform


''' Carga los DataFrames de Train y Test parseando las fechas de las
    columnas de manera adecuada.
    Recibe:
        - Directorios de los DataFrames a cargar como kwargs:
            - dirTrain
            - dirTest
            - dirWeather
            - dirStation
    Devuelve:
        - Tupla con los DataFrames. '''
def loadDataFrames(**kwargs) :

    if len(kwargs) < 1 :
        raise TypeError('loadDataFrames() recibe al menos un keyword arg.')

    possible_values = { 'dirTrain':None,
                        'dirTest':None,
                        'dirStation':None,
                        'dirWeather':None }

    for key, value in possible_values.items() :

        date_names = ['start_date', 'end_date'] if (key == 'dirTrain' or key == 'dirTest') else ['date']

        if key == 'dirStation' :
            date_names = ['installation_date']

        if key in kwargs :
            possible_values[key] = pd.read_csv(kwargs[key],
                                               parse_dates=date_names,
                                               infer_datetime_format=True)

    dataFrames = ()
    for dataFrame in [possible_values['dirTrain'], possible_values['dirTest'], possible_values['dirStation'], possible_values['dirWeather']] :
        if dataFrame is not None :
            dataFrames += (dataFrame, )

    return dataFrames

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
