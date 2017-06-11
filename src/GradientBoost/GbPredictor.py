#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.ensemble import GradientBoostingRegressor
import src.utils as utils

def predict(train, target, testIds, testVals, estimators):

    gb = GradientBoostingRegressor(n_estimators=estimators)
    print("Gradient Boosting - Volcando puntos...")
    gb.fit(train, target)

    print("Gradient Boosting - Prediciendo...")
    predictions = gb.predict(testVals)

    return predictions