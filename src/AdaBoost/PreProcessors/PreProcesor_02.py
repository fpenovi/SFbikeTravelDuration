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
    dfTrain = dfTrain[['id', 'duration',
                       'start_date', 'start_station_id',
                       'subscription_type']]

    dfTest = dfTest[['id', 'start_date',
                     'start_station_id',
                     'subscription_type']]

    dfTrain['Order'] = pd.Series(xrange(len(dfTrain)))
    dfTest['Order'] = pd.Series(xrange(len(dfTest)))
    dfWeather = dfWeather[['date', 'zip_code', 'mean_temperature_f', 'events']]

    # Agrego columnas con la informacion de fechas a los dataframes
    dates = {'year':dfTrain.start_date.dt.year,
             'month':dfTrain.start_date.dt.month,
             'day':dfTrain.start_date.dt.dayofyear,
             'weekday':dfTrain.start_date.dt.dayofweek,
             'hour':dfTrain.start_date.dt.hour}

    wdates = {'year':dfWeather.date.dt.year,
              'month':dfWeather.date.dt.month,
              'day':dfWeather.date.dt.dayofyear}

    dfTrain = dfTrain.join(pd.DataFrame(dates))

    dates = {'year':dfTest.start_date.dt.year,
             'month':dfTest.start_date.dt.month,
             'day':dfTest.start_date.dt.dayofyear,
             'weekday':dfTest.start_date.dt.dayofweek,
             'hour':dfTest.start_date.dt.hour}

    dfTest = dfTest.join(pd.DataFrame(dates))

    # Armo el DataFrame del clima con Year Month Day Zip_code como claves para poder mergear
    dfWeather = dfWeather.join(pd.DataFrame(wdates))[['year', 'month', 'day', 'zip_code',
                                                      'mean_temperature_f', 'events']]

    # Reordeno las columnas
    dfTrain = dfTrain[['Order', 'id', 'duration', 'year',
                       'month', 'weekday', 'day',
                       'hour', 'start_station_id',
                       'subscription_type']]

    dfTest = dfTest[['Order', 'id', 'year', 'month',
                     'weekday', 'day',
                     'hour', 'start_station_id',
                     'subscription_type']]

    # Preparo el STATION dataframe
    dfStation.loc[:,'city'] = dfStation.apply(utils.cityNameToZipCode, axis=1)
    dfStation.rename(columns={'id':'start_station_id', 'city':'zip_code'}, inplace=True)
    dfStation = dfStation[['start_station_id', 'zip_code']]

    # ***************REALIZO LOS MERGE CON AMBOS DATAFRAMES DE STATION Y WEATHER***************
    dfTrain = dfTrain.merge(dfStation, on='start_station_id')[['Order', 'id', 'duration',
                                                               'start_station_id', 'subscription_type',
                                                               'weekday', 'year', 'month', 'day',
                                                               'hour', 'zip_code']]

    dfTest = dfTest.merge(dfStation, on='start_station_id')[['Order', 'id',
                                                               'start_station_id', 'subscription_type',
                                                               'weekday', 'year', 'month', 'day',
                                                               'hour', 'zip_code']]

    dfTrain = dfTrain.merge(dfWeather, on=['year', 'month', 'day', 'zip_code'])
    dfTest = dfTest.merge(dfWeather, on=['year', 'month', 'day', 'zip_code'])
    # ****************************************************************************************

    # Elimino las rows sin muestreo de temperatura en set de TRAIN
    dfTrain = dfTrain.loc[~dfTrain.mean_temperature_f.isnull()]

    # Completo los NaN en el set de TRAIN
    # dfTrain.mean_temperature_f = dfTrain.apply(utils.setMeanTemperature, axis=1)
    # dfTrain.mean_wind_speed_mph = dfTrain.apply(utils.setMeanWindSpeed, axis=1)
    dfTrain.events = dfTrain.apply(utils.fillEvents, axis=1)

    # Completo los NaN en el set de TEST
    dfTest.mean_temperature_f = dfTest.apply(utils.setMeanTemperature, axis=1)
    dfTest.events = dfTest.apply(utils.fillEvents, axis=1)
    # dfTest.mean_wind_speed_mph = dfTest.apply(utils.setMeanWindSpeed, axis=1)

    # Cambio los events por enteros
    eventTypes = dfTrain.events.unique()
    dfTrain.events = dfTrain.events.astype('category', categories=eventTypes).cat.codes
    dfTest.events = dfTest.events.astype('category', categories=eventTypes).cat.codes

    # Vuelvo al orden original
    dfTrain.sort_values(by='Order', inplace=True)
    dfTest.sort_values(by='Order', inplace=True)

    # GENERO TARGET, TRAIN, TEST Y TESTIDS
    target = dfTrain.duration
    testIds = dfTest.id
    dfTrain.drop(['Order', 'id', 'duration', 'zip_code'], axis=1, inplace=True)
    dfTest.drop(['Order', 'id', 'zip_code'], axis=1, inplace=True)

    return dfTrain, target, testIds, dfTest
