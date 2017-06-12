#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
from sklearn.neural_network import MLPRegressor
import src.utils as utils


def predict(train, target, testIds, testVals, alpha=None):

    alpha = 0.001 if (alpha is None) else alpha

    mlp = MLPRegressor(hidden_layer_sizes=(100,),  activation='identity', solver='lbfgs', alpha=alpha, batch_size='auto',
                       learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
                       random_state=0, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
                       early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

    print("MLP - Volcando puntos...")
    mlp.fit(train, target)

    print("MLP - Prediciendo...")
    predictions = mlp.predict(testVals)

    return predictions
