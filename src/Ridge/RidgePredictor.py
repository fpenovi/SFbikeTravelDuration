#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.linear_model import Ridge
import csv
import sys
import src.utils as utils

def predict(train, target, testIds, testVals):

    ridge = Ridge(alpha=10.0, fit_intercept=True, normalize=False,
             copy_X=True, max_iter=None, tol=0.001,
             solver='svd', random_state=0)

    print("Ridge - Volcando puntos...")
    ridge.fit(train, target)

    print("Ridge - Prediciendo...")
    predictions = ridge.predict(testVals)

    return predictions
