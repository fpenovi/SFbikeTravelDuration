#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import src.utils as utils

''' Carga y preprocesa los datos en los CSV de forma equivalente para poder
    ser utilizados para un Random Forest.

    Recibe:
        - dirTrain: directorio del train.csv
        - dirTest: directorio del test.csv
    Devuelve:
        - Tupla -> (DataFrameTrain, SeriesTarget, SeriesTestIDs, DataFrameTest)'''
def loadData(dirTrain, dirTest, dirStation, dirWeather) :

    dfTrain, dfTest, dfStation, dfWeather = utils.loadDataFrames(dirTrain=dirTrain, dirTest=dirTest, dirStation=dirStation, dirWeather=dirWeather)

    # Convierto a los SUSCRIBER en un 0
    # Convierto a los CUSTOMER en un 1
    subscriptionTypes = dfTrain.subscription_type.unique()

    # Reemplazo por 0 y 1
    dfTrain.subscription_type = dfTrain.subscription_type.astype('category', categories=subscriptionTypes).cat.codes
    dfTest.subscription_type = dfTest.subscription_type.astype('category', categories=subscriptionTypes).cat.codes

    # NO FILTRO los registros con duraciones excesivas ya que KNN la rompe con todos los datos

    trainDateData = {'year':dfTrain.start_date.dt.year,
                     'month':dfTrain.start_date.dt.month,
                     'day':dfTrain.start_date.dt.dayofyear,
                     'weekday':dfTrain.start_date.dt.dayofweek,
                     'hour':dfTrain.start_date.dt.hour}

    testDateData = {'year':dfTest.start_date.dt.year,
                    'month':dfTest.start_date.dt.month,
                    'day':dfTest.start_date.dt.dayofyear,
                    'weekday':dfTest.start_date.dt.dayofweek,
                    'hour':dfTest.start_date.dt.hour}

    # Para hacer el join con los train y test
    wdates = {'year':dfWeather.date.dt.year,
              'month':dfWeather.date.dt.month,
              'day':dfWeather.date.dt.dayofyear}

    # Agrego columnas con la informacion de fechas a los dataframes
    dfTrain = dfTrain.join(pd.DataFrame(trainDateData))
    dfTest = dfTest.join(pd.DataFrame(testDateData))

    # Armo el DataFrame del clima con Year Month Day Zip_code como claves para poder mergear
    dfWeather = dfWeather.join(pd.DataFrame(wdates))[['year', 'month', 'day', 'zip_code',
                                                  'mean_temperature_f', 'mean_dew_point_f',
                                                  'mean_humidity', 'mean_sea_level_pressure_inches',
                                                  'mean_visibility_miles', 'mean_wind_speed_mph',
                                                  'precipitation_inches']]
    # Reordeno las columnas
    dfTrain = dfTrain[['id', 'duration', 'year',
                   'month', 'weekday', 'day',
                   'hour', 'start_station_id',
                   'subscription_type']]

    dfTest = dfTest[['id', 'year',
                     'month', 'weekday', 'day',
                     'hour', 'start_station_id',
                     'subscription_type']]

    # Normalizo el Station DataFrame para poder mergear por station_id
    dfStation.loc[:,'city'] = dfStation.apply(utils.cityNameToZipCode, axis=1)
    dfStation.rename(columns={'id':'start_station_id', 'city':'zip_code'}, inplace=True)
    dfStation = dfStation[['start_station_id', 'zip_code']]

    # ***************REALIZO LOS MERGE CON AMBOS DATAFRAMES DE STATION Y WEATHER***************
    dfTrain = dfTrain.merge(dfStation, on='start_station_id')[['id', 'duration',
                                                           'start_station_id', 'subscription_type',
                                                           'weekday', 'year', 'month', 'day',
                                                           'zip_code']]

    dfTrain = dfTrain.merge(dfWeather, on=['year', 'month', 'day', 'zip_code'])

    dfTest = dfTest.merge(dfStation, on='start_station_id')[['id',
                                                           'start_station_id', 'subscription_type',
                                                           'weekday', 'year', 'month', 'day',
                                                           'zip_code']]

    dfTest = dfTest.merge(dfWeather, on=['year', 'month', 'day', 'zip_code'])
    # ****************************************************************************************

    # Remuevo las columnas de id y duracion
    dfTrain.drop(['zip_code', 'mean_sea_level_pressure_inches', 'mean_visibility_miles', 'precipitation_inches', 'mean_dew_point_f', 'mean_wind_speed_mph', 'mean_humidity', 'year', 'mean_temperature_f'], axis=1 , inplace=True)
    dfTest.drop(['zip_code', 'mean_sea_level_pressure_inches', 'mean_visibility_miles', 'precipitation_inches', 'mean_dew_point_f', 'mean_wind_speed_mph', 'mean_humidity', 'year', 'mean_temperature_f'], axis=1 , inplace=True)

    dfTrain = dfTrain.dropna()
    dfTest = dfTest.dropna()

    # GENERO TARGET, TRAIN, TEST Y TESTIDS (testids para el output)
    target = dfTrain.duration
    testIds = dfTest.id

    dfTrain.drop(['id','duration'], axis=1, inplace=True)
    dfTest.drop(['id'], axis=1, inplace=True)

    print dfTrain

    return dfTrain, target, testIds, dfTest
