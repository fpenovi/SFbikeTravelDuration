#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.linear_model import Ridge
import csv
import sys
import src.utils as utils

def predict(train, target, testIds, testVals):

    ridge = Ridge()
    print("Ridge - Volcando puntos...")
    ridge.fit(train, target)

    print("Ridge - Prediciendo...")
    predictions = ridge.predict(testVals)

    return predictions
