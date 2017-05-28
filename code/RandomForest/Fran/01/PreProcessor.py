#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

#	**************************************************************************************************************************************
#	Tutorial scikit-learn Random Forest:
# 	http://www.agcross.com/2015/02/random-forests-in-python-with-scikit-learn/
#	**************************************************************************************************************************************

''' Carga y preprocesa los datos en los CSV de forma equivalente para poder
    ser utilizados para un Random Forest.

    Recibe:
        - dirTrain: directorio del train.csv
        - dirTest: directorio del test.csv
    Devuelve:
        - Tupla -> (DataFrameTrain, SeriesTarget, SeriesTestIDs, DataFrameTest)'''
def loadData(dirTrain, dirTest) :

    dfTrain = pd.read_csv(dirTrain,
                          parse_dates=['start_date', 'end_date'],
                          infer_datetime_format=True)

    dfTest = pd.read_csv(dirTest,
                         parse_dates=['start_date', 'end_date'],
                         infer_datetime_format=True)

    # Convierto a los SUSCRIBER en un 0
    # Convierto a los CUSTOMER en un 1
    subscriptionTypes = dfTrain.subscription_type.unique()

    # Reemplazo por 0 y 1
    dfTrain.subscription_type = dfTrain.subscription_type.astype('category', categories=subscriptionTypes).cat.codes
    dfTest.subscription_type = dfTest.subscription_type.astype('category', categories=subscriptionTypes).cat.codes

    # GENERO TARGET, TRAIN, TEST Y TESTIDS (testids para el output)
    target = dfTrain.duration
    testIds = dfTest['id']


    trainDateData = {'start_month':dfTrain.start_date.dt.month,
                     'start_dayOfYear':dfTrain.start_date.dt.dayofyear,
                     'start_dayOfWeek':dfTrain.start_date.dt.dayofweek,
                     'start_hourOfDay':dfTrain.start_date.dt.hour}

    testDateData = {'start_month':dfTest.start_date.dt.month,
                    'start_dayOfYear':dfTest.start_date.dt.dayofyear,
                    'start_dayOfWeek':dfTest.start_date.dt.dayofweek,
                    'start_hourOfDay':dfTest.start_date.dt.hour}

    # Agrego columnas con la informacion de fechas a los dataframes
    dfTrain = dfTrain[['start_station_id', 'subscription_type']].join(pd.DataFrame(trainDateData), how='outer')
    dfTest = dfTest[['start_station_id', 'subscription_type']].join(pd.DataFrame(testDateData), how='outer')

    return dfTrain, target, testIds, dfTest
