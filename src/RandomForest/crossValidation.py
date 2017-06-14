#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
from importlib import import_module
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import src.utils as utils

def main():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)

	if (len(sys.argv) < 4):
		print("Modo de uso -> python main.py <pre_processing_module> <n_from> <n_to>")
		return 0

	pre_proc = sys.argv[1]
	n_from = sys.argv[2]
	n_to = sys.argv[3]

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
	if (not n_from.isdigit()) :
		print ("Error: Parámetro n_from debe ser numérico")
		return 1

	if (not n_to.isdigit()):
		print("Error: Parámetro n_to debe ser numérico")
		return 1

	n_from = int(n_from)
	n_to = int(n_to)

	if (not n_from < n_to):
		print("Error: Parámetro n_from debe ser menor a n_to")
		return 1
	# --------------------------------------------------------------------------------------------------------#

	print("Preprocesando datos")
	train, target, testIds, testVals = PreProcessor.loadData(	'../../DataSet/trip_train.csv',
																'../../DataSet/trip_test.csv',
																'../../DataSet/station.csv',
																'../../DataSet/weather.csv')
	kValues = utils.primeNumbersBetween(n_from, n_to)
	cvErrors = []
	print ("Realizando cross validation de Random Forest con n_estimators primos entre %d y %d." % (n_from, n_to))
	for k in kValues:

		rf = RandomForestRegressor(n_estimators=k, criterion='mse', max_depth=None,
			                       min_samples_split=2, min_samples_leaf=1,
			                       min_weight_fraction_leaf=0.0, max_features='auto',
			                       max_leaf_nodes=None, min_impurity_split=1e-07,
			                       bootstrap=True, oob_score=False, n_jobs=1,
			                       random_state=0, verbose=0, warm_start=False)

		errors = cross_val_score(rf, train, target, scoring='neg_mean_squared_error')
		# Tomo el promedio de los diferentes errores e invierto su valor por ser negativo
		cvErrors.append(-errors.mean())

	# ----------------------------------------------------- Plot ----------------------------------------------#

	print ("Realizando plot")
	# Obtengo k optimo
	nOptimo = kValues[cvErrors.index(min(cvErrors))]
	plt.figure().suptitle('Cross validation for Random Forest - N optimo ' + str(nOptimo), fontsize=20)
	plt.plot(kValues, cvErrors)
	plt.xlabel('Number of Estimators N')
	plt.ylabel('Mean squared error')
	plt.xlim(kValues[0], kValues[-1])
	plt.xticks(kValues, kValues, rotation='vertical')
	plt.gcf().set_size_inches(18,7, forward = True)
	plt.show()

main()
