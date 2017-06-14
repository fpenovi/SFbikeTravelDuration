#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import platform
import csv
import math

DISTANCES = {-3:'jaccard', -2:'braycurtis', -1:'canberra', 0:'hamming', 1:'manhattan', 2:'euclidean'}


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

''' Categoriza un evento meteorológico del set de datos 'weather.csv'
    como 'Clear', 'Rain' o 'Rain-thunderstorm'''
def getEventCategoryName(event):
    if pd.isnull(event):
        return 'Clear'
    capitalizedEvent = event.capitalize()
    if capitalizedEvent == 'Fog':
        return 'Clear'
    if capitalizedEvent == 'Fog-rain':
        return 'Rain'
    return capitalizedEvent

def setMeanTemperature(row) :
    if np.isnan(row.mean_temperature_f) :

        temps = { 94107:[50.0, 52.5, 54.5, 56.5, 56.5, 59.0, 66.0, 64.5, 62.5, 61.0, 56.5, 50.5], # San Francisco
                  94063:[49.0, 52.5, 55.0, 57.5, 62.0, 66.0, 68.0, 68.5, 67.0, 62.0, 54.5, 49.0], # Redwood City
                  94301:[48.0, 51.5, 54.5, 57.5, 61.5, 65.0, 68.0, 67.0, 66.5, 61.0, 53.5, 48.0], # Palo Alto
                  94041:[51.0, 53.5, 56.0, 59.0, 62.5, 66.5, 68.0, 68.0, 68.0, 63.5, 56.0, 51.0], # Mountain View
                  95113:[51.0, 54.5, 57.0, 59.5, 64.0, 68.5, 71.0, 71.0, 69.5, 64.5, 56.5, 51.5]} # San Jose

        return temps[row.zip_code][int(row.month) - 1]

    return row.mean_temperature_f

def setMeanWindSpeed(row) :
    if np.isnan(row.mean_wind_speed_mph) :

        speed = { 94107:[7.0, 8.0, 10.0, 12.0, 14.0, 14.0, 13.0, 12.0, 11.0, 9.0, 7.0, 7.0], # San Francisco
                  94063:[7.0, 8.0, 9.0, 10.0, 11.0, 11.0, 11.0, 10.0, 9.0, 8.0, 7.0, 7.0],   # Redwood City
                  94301:[6.0, 7.0, 9.0, 10.0, 10.0, 11.0, 10.0, 10.0, 9.0, 7.0, 6.0, 6.0],   # Palo Alto
                  94041:[6.0, 7.0, 9.0, 10.0, 10.0, 11.0, 10.0, 10.0, 9.0, 7.0, 6.0, 6.0],   # Mountain View
                  95113:[5.0, 6.0, 6.0, 7.0, 8.0, 8.0, 7.0, 7.0, 6.0, 5.0, 5.0, 5.0]}        # San Jose

        return speed[row.zip_code][int(row.month) - 1]

    return row.mean_wind_speed_mph

def fillEvents(row) :
    if pd.isnull(row.events) :
        return 'Clear'

    if 'rain' in row.events.lower() :
        return 'Rain'

    if 'fog' in row.events.lower() :
        return 'Fog'

def getSystemWriteMode() :
    if platform.system() == 'Windows' :
        return 'wb'

    return 'w'

def exportResults(predictions, testIds, filename) :

    print("Guardando a archivo...")

    with open(filename, getSystemWriteMode()) as outfile:
        rows = [["id", "duration"]]

        for idTest, prediction in zip(testIds, predictions):
            rows.append([idTest, prediction])

        out_csv = csv.writer(outfile)
        out_csv.writerows(rows)

    print("Se guardó a " + filename + " exitosamente")

'''Devuelve los numeros primos entre min_number y max_number'''
def primeNumbersBetween(min_number, max_number):
    primes = []
    #Si es menor o igual a dos lo agrego para descartar pares
    if (min_number <= 2):
        primes.append(2)
    #Si es par lo descarto y avanzo al próximo impar
    if (min_number%2 == 0):
        min_number = min_number + 1

    for num in range(min_number, max_number + 1, 2):
        if all(num%i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
           primes.append(num)
    return primes
