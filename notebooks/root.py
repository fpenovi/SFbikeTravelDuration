# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns             # Libreria muy buena de plots
import cfg as cfg                 # Importo archivo de configuración

dfStation = pd.read_csv(cfg.STATION_CSV, parse_dates=['installation_date'], infer_datetime_format=True)
# dfStatus = pd.read_csv(cfg.STATUS_CSV)   OJO CON ESTE QUE ES MUY PESADO
dfTrip = pd.read_csv(cfg.TRIP_CSV, parse_dates=['start_date', 'end_date'], infer_datetime_format=True)
dfWeather = pd.read_csv(cfg.WEATHER_CSV, parse_dates=['date'], infer_datetime_format=True)

''' Recibe un plot de barras y les asigna sus valores
    encima de cada una de ellas. Se puede setear textsize y alpha.'''
def autolabel(ax, textsize, alpha):
    # Get y-axis height to calculate label position from.
    (y_bottom, y_top) = ax.get_ylim()
    y_height = y_top - y_bottom

    for rect in ax.patches:
        height = rect.get_height()
        label_position = height + (y_height * 0.01)

        ax.text(rect.get_x() + rect.get_width()/2., label_position,
                '%d' % int(height),
                ha='center', va='bottom', size=textsize, alpha=alpha)


''' Utilizada como parámetro para función DataFrame.apply
    Para cada row, devuelve el zip code correspondiente a la ciudad.'''
def cityNameToZipCode(row) :

    if row.city == 'San Francisco' :
        return '94107'

    if row.city == 'Redwood City' :
        return '94063'

    if row.city == 'Palo Alto' :
        return '94301'

    if row.city == 'Mountain View' :
        return '94041'

    if row.city == 'San Jose' :
        return '95113'

    raise ValueError('Malo malo!')


''' Utilizada para generar un DataFrame nuevo que contiene las filas de la ciudad
    pasada por parámetro únicamente.'''
def makeNewDataFrameWithCity(df, city) :

    dic = {'date':[], 'city':[], 'zip_code':[], 'duration':[], 'max_temp_f':[], 'min_temp_f':[]}

    for i in range(0, len(df)):
        if (df.iloc[i]['city'] == city ) :
            dic['date'].append(df.iloc[i]['date'])
            dic['city'].append(df.iloc[i]['city'])
            dic['zip_code'].append(df.iloc[i]['zip_code'])
            dic['duration'].append(df.iloc[i]['duration'])
            dic['max_temp_f'].append(df.iloc[i]['max_temperature_f'])
            dic['min_temp_f'].append(df.iloc[i]['min_temperature_f'])

    return pd.DataFrame.from_dict(data=dic, orient='columns')


''' Utilizada para clasificar en grupos a las horas del día.'''
def getMomentOfDay(row):
    
    if row.hour < 5:
        return 'Late night'
    if  5 <= row.hour < 12:
        return 'Morning'
    if 12 <= row.hour < 14:
        return 'Noon'
    if 14 <= row.hour < 18:
        return 'Afternoon'
    if 18 <= row.hour < 21:
        return 'Evening'
    if 21 <= row.hour <= 23:
        return 'Night'
