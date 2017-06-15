#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import sys
from sklearn.preprocessing import StandardScaler
from src.NearestNeighbours import KnnPredictor
from src.RandomForest import RfPredictor
from src.GradientBoost import GbPredictor
from src.Ridge import RidgePredictor
from src.AdaBoost import AbPredictor
from src.MultiLayerPerceptron import MultiLayerPerceptronPredictor
from importlib import import_module
import src.validator as validator
import time
import src.utils as utils

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
	predictors = ["KNN", "RANDOM FOREST", "ADA BOOST"]
	predictions = [	KnnPredictor.predict(train, target, testIds, testVals, 821, 1),
					RfPredictor.predict(train, target, testIds, testVals, 401),
					AbPredictor.predict(train, target, testIds, testVals, 5)]

	#Tomo los errors de cada uno de los predictores
	errors = []
	for prediction,predictorName in zip(predictions,predictors):
		error = validator.getOutputScore(testIds,prediction)
		print 'Error de %s: %f' % (predictorName, error)
		errors.append(error)

	# Permito que python libere la memoria
	train = None
	target = None
	testVals = None

	#Calculo la prediccion final mediante promedio ponderado
	finalPrediction = map(lambda pred: mean(errors, pred), zip(*predictions))

	print 'Error del promedio final:', validator.getOutputScore(testIds, finalPrediction)

	filename = "combination.csv"
	utils.exportResults(finalPrediction, testIds, filename)

	end = time.time()
	m, s = divmod(end - start, 60)
	h, m = divmod(m, 60)
	print 'Tiempo:', "%02d:%02d:%02d" % (h, m, s)

	return 0

'''	Calcula el promedio a ser utilizado para la combinacion.'''
def mean(scores, predictions):
	suma = 0
	divisor = 0
	for prediction,score in zip(predictions,scores):
		suma += float(prediction)/score
		divisor += 1/score
	return suma / divisor

combinate()