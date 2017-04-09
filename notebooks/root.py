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
