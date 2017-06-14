#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestRegressor
import csv
import sys
import src.utils as utils

def predict(train, target, testIds, testVals, estimators):

    rf = RandomForestRegressor(n_estimators=estimators, n_jobs=-1, random_state=0) 	# Jobs = -1 elije numero de
                                                                    # jobs segun cantidad de cores.
    print("RF - Volcando puntos...")
    rf.fit(train, target)

    print("RF - Prediciendo...")
    predictions = rf.predict(testVals)

    return predictions
