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
