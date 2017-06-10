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

    dfTrain, dfTest, dfStation = utils.loadDataFrames(dirTrain=dirTrain, dirTest=dirTest, dirStation=dirStation)

    # Convierto a los SUSCRIBER en un 0
    # Convierto a los CUSTOMER en un 1
    subscriptionTypes = dfTrain.subscription_type.unique()

    # Reemplazo por 0 y 1
    dfTrain.subscription_type = dfTrain.subscription_type.astype('category', categories=subscriptionTypes).cat.codes
    dfTest.subscription_type = dfTest.subscription_type.astype('category', categories=subscriptionTypes).cat.codes

    # NO FILTRO los registros con duraciones excesivas ya que KNN la rompe con todos los datos

    # GENERO TARGET, TRAIN, TEST Y TESTIDS (testids para el output)
    target = dfTrain.duration
    testIds = dfTest['id']


    trainDateData = {'month':dfTrain.start_date.dt.month,
                     'day':dfTrain.start_date.dt.dayofyear,
                     'weekday':dfTrain.start_date.dt.dayofweek,
                     'hour':dfTrain.start_date.dt.hour}

    testDateData = {'month':dfTest.start_date.dt.month,
                    'day':dfTest.start_date.dt.dayofyear,
                    'weekday':dfTest.start_date.dt.dayofweek,
                    'hour':dfTest.start_date.dt.hour}

    # Agrego columnas con la informacion de fechas a los dataframes
    dfTrain = dfTrain[['start_station_id']].join(pd.DataFrame(trainDateData))
    dfTest = dfTest[['start_station_id']].join(pd.DataFrame(testDateData))

    dfStation.rename(columns={'id':'start_station_id'}, inplace=True)
    dfStation = dfStation[['start_station_id', 'city']]
    cities = dfStation.city.unique()
    dfStation.city = dfStation.city.astype('category', categories=cities).cat.codes

    dfTrain = dfTrain.merge(dfStation, on='start_station_id')
    dfTest = dfTest.merge(dfStation, on='start_station_id')

    return dfTrain, target, testIds, dfTest
