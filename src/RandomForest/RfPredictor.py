#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestRegressor
import csv
import sys
import src.utils as utils

def predict(train, target, testIds, testVals, estimators) :

    rf = RandomForestRegressor(n_estimators=estimators, criterion='mse', max_depth=None,
                               min_samples_split=2, min_samples_leaf=50,
                               min_weight_fraction_leaf=0.0, max_features='auto',
                               max_leaf_nodes=None, min_impurity_split=1e-07,
                               bootstrap=True, oob_score=False, n_jobs=-1,
                               random_state=0, verbose=0, warm_start=False) 	# Jobs = -1 elije numero de
                                                                                # jobs segun cantidad de cores.
    print("RF - Volcando puntos...")
    rf.fit(train, target)

    print("RF - Prediciendo...")
    predictions = rf.predict(testVals)

    return predictions
