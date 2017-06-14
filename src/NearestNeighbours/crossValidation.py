#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
from importlib import import_module
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score
import src.utils as utils
from src.utils import DISTANCES


def main():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)

	if (len(sys.argv) < 4):
		print("Modo de uso -> python main.py <pre_processing_module> <k_from> <k_to> [distance=2]")
		return 0

	pre_proc = sys.argv[1]
	k_from = sys.argv[2]
	k_to = sys.argv[3]
	distancia = sys.argv[4] if len(sys.argv) == 5 else 2    # Euclidea por defecto

	# ----------------------------------------- Validación de argumentos -------------------------------------#
	if (not pre_proc.isdigit() or len(pre_proc) < 2) :
		print ("Error: Parámetro pre_processing_module debe ser numérico y de dos caracteres (i.e: '01').")
		return 1

	try:
		PreProcessor = import_module('PreProcessors.PreProcesor_' + pre_proc)
	except ImportError as e:
		print ("Error importando el preprocesador: '" + pre_proc + "'.")
		print ("Error:", e)
		return 1
	if (not k_from.isdigit()) :
		print ("Error: Parámetro k_from debe ser numérico")
		return 1

	if (not k_to.isdigit()):
		print("Error: Parámetro k_to debe ser numérico")
		return 1

	try:
		distancia = int(distancia)
	except ValueError as e:
		print "Error: Parámetro distancia debe ser numérico"
		return 1

	metric = DISTANCES[int(distancia)] if (distancia in DISTANCES) else 'minkowski'
	p = int(distancia) if(metric not in DISTANCES) else None
	k_from = int(k_from)
	k_to = int(k_to)
	s_algorithm = 'ball_tree' if (distance < 1) else 'kd_tree'

	if (not k_from < k_to):
		print("Error: Parámetro k_from debe ser menor a k_to")
		return 1
	# --------------------------------------------------------------------------------------------------------#

	print("Preprocesando datos")
	train, target, testIds, testVals = PreProcessor.loadData(	'../../DataSet/trip_train.csv',
																'../../DataSet/trip_test.csv',
																'../../DataSet/station.csv',
																'../../DataSet/weather.csv')
	kValues = utils.primeNumbersBetween(k_from, k_to)
	cvErrors = []
	print ("Realizando cross validation de KNN para los K primos entre %d y %d con métrica %s" % (k_from, k_to, metric))
	for k in kValues:
		knn = KNeighborsRegressor(	n_neighbors = k, n_jobs = -1,
								 	weights='distance', algorithm = s_algorithm,
								 	leaf_size=30, p = p, metric = metric)
		errors = cross_val_score(	knn, train, target,
									scoring = 'neg_mean_squared_error')
		# Tomo el promedio de los diferentes errores e invierto su valor por ser negativo
		cvErrors.append(-errors.mean())

	# ----------------------------------------------------- Plot ----------------------------------------------#

	print ("Realizando plot")
	# Obtengo k optimo
	kOptimo = kValues[cvErrors.index(min(cvErrors))]
	plt.figure().suptitle('Cross validation for KNN - K optimo ' + str(kOptimo), fontsize=20)
	plt.plot(kValues, cvErrors)
	plt.xlabel('Number of Neighbors K')
	plt.ylabel('Mean squared error')
	plt.xlim(kValues[0], kValues[-1])
	plt.xticks(kValues, kValues, rotation='vertical')
	plt.gcf().set_size_inches(18,7, forward = True)
	plt.show()

main()
