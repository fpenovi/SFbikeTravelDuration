#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.ensemble import AdaBoostRegressor
import csv
import sys
import src.utils as utils

def predict(train, target, testIds, testVals, estimators):

    ab = AdaBoostRegressor(n_estimators=estimators, loss='square', random_state=1)
    print("AdaBoost - Volcando puntos...")
    ab.fit(train, target)

    print("AdaBoost - Prediciendo...")
    predictions = ab.predict(testVals)

    return predictions
