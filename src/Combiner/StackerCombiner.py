#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import Ridge
from importlib import import_module
import src.validator as validator
import time
import src.utils as utils
from mlxtend.regressor import StackingRegressor


def combinate():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)

	start = time.time()     # Arranco a contar el tiempo
	print('Cargando y Preprocesando datos...')
	try:
		PreProcessor = import_module('PreProcessors.PreProcesor_02')
	except ImportError as e:
		print("Error importando el preprocesador.")
		print "Error:", e
		return 1
	train, target, testIds, testVals = PreProcessor.loadData('../../DataSet/trip_train.csv',
                                                             '../../DataSet/trip_test.csv',
                                                             '../../DataSet/station.csv',
                                                             '../../DataSet/weather.csv')
	print 'Estandarizando data sets...'
	scaler = StandardScaler().fit(train)
	train = scaler.transform(train)
	testVals = scaler.transform(testVals)
	regressors = [	KNeighborsRegressor(n_neighbors=707, weights='distance',
                              algorithm='kd_tree', leaf_size=30, p=1,
                              metric='manhattan', metric_params=None, n_jobs=-1),
					RandomForestRegressor(n_estimators=307, n_jobs=-1, random_state=0), 
					AdaBoostRegressor(n_estimators=5, loss='square', random_state=1)]

	stregr = StackingRegressor(regressors = regressors, meta_regressor = Ridge())
	print ("Cargando los modelos")
	stregr.fit(train, target)

	#Calculo la prediccion final mediante promedio ponderado
	print("Prediciendo")
	finalPrediction = stregr.predict(testVals)

	print 'Error del promedio final:', validator.getOutputScore(testIds, finalPrediction)

	filename = "combination.csv"
	utils.exportResults(finalPrediction, testIds, filename)

	end = time.time()
	m, s = divmod(end - start, 60)
	h, m = divmod(m, 60)
	print 'Tiempo:', "%02d:%02d:%02d" % (h, m, s)

	return 0

'''	Calcula el promedio a ser utilizado para la combinacion.'''
#def mean(scores, predictions):
#	suma = 0
#	divisor = 0
#	for prediction,score in zip(predictions,scores):
#		suma += float(prediction)/score
#		divisor += 1/score
#	return suma / divisor

def mean(scores, predictions):
	return reduce(lambda x, y: x + y, predictions) / len(predictions)

combinate()