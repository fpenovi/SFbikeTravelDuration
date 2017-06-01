#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import src.utils as utils

def loadData(dirTrain, dirTest, dirStation, dirWeather) :
	dfTrain, dfTest, dfStation, dfWeather = utils.loadDataFrames(dirTrain=dirTrain, dirTest=dirTest, dirStation=dirStation, dirWeather=dirWeather)

	dfWeather = dfWeather[['date', 'zip_code', 'events', 'precipitation_inches']]
	dfWeather.rename(columns={'date':'start_date'}, inplace=True)
	dfWeather.events = dfWeather.events.apply(utils.getEventCategoryName)

    #Convierto a 0,1,2,3,4 de acuerdo al tipo de evento
	events = dfWeather.events.unique()
	dfWeather.events = dfWeather.events.astype('category', categories=events).cat.codes
	dfStation.rename(columns={'id':'start_station_id'}, inplace=True)

	#Recorto del train los viajes cuya duración es ESTUPIDA
	dfTrain = dfTrain[(60*2 <= dfTrain.duration) & (dfTrain.duration <= 3600*6)]
	#Agrego columna de events a dfTrain
	dfTrain = dfTrain.merge(dfStation[['start_station_id', 'city']], on=['start_station_id'])
	dfTrain.zip_code = dfTrain.apply(utils.cityNameToZipCode, axis=1)
	dfTrain.start_date = pd.to_datetime(dfTrain.start_date.dt.date)
	dfTrain = dfTrain.merge(dfWeather, on=['start_date', 'zip_code'])

	#Agrego columna de events a dfTest
	dfTest = dfTest.merge(dfStation[['start_station_id', 'city']], on=['start_station_id'])
	dfTest.zip_code = dfTest.apply(utils.cityNameToZipCode, axis=1)
	dfTest.start_date = pd.to_datetime(dfTest.start_date.dt.date)
	dfTest = dfTest.merge(dfWeather, on=['start_date', 'zip_code'])

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
                     'start_dayOfWeek':dfTrain.start_date.dt.dayofweek,
                     'start_hourOfDay':dfTrain.start_date.dt.hour,
                     'start_year':dfTrain.start_date.dt.year,
                     'start_dayOfYear':dfTrain.start_date.dt.dayofyear}

	testDateData = {'start_month':dfTest.start_date.dt.month,
                    'start_dayOfWeek':dfTest.start_date.dt.dayofweek,
                    'start_hourOfDay':dfTest.start_date.dt.hour,
                    'start_year':dfTest.start_date.dt.year,
                    'start_dayOfYear':dfTest.start_date.dt.dayofyear}

	# Agrego columnas con la informacion de fechas a los dataframes
	dfTrain = dfTrain[['start_station_id', 'subscription_type', 'events']].join(pd.DataFrame(trainDateData), how='outer')
	dfTest = dfTest[['start_station_id', 'subscription_type', 'events']].join(pd.DataFrame(testDateData), how='outer')

	return dfTrain, target, testIds, dfTest