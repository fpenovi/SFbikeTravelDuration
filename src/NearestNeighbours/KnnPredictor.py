#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.neighbors import KNeighborsRegressor
import csv
import sys
import src.utils as utils

DISTANCES = {-3:'jaccard', -2:'braycurtis', -1:'canberra', 0:'hamming', 1:'manhattan', 2:'euclidean'}

def predict(train, target, testIds, testVals, neighbors, distance=2):

    m_distance = DISTANCES[distance] if (distance in DISTANCES) else 'minkowski'
    p_distance = distance if (m_distance not in DISTANCES) else None
    s_algorithm = 'ball_tree' if (distance < 1) else 'kd_tree'

    knn = KNeighborsRegressor(n_neighbors=neighbors, weights='distance',
                              algorithm=s_algorithm, leaf_size=30, p=p_distance,
                              metric=m_distance, metric_params=None, n_jobs=-1)     # Jobs = -1 elije numero de
                                                                                    # jobs segun cantidad de cores.
    print("KNN - Volcando puntos...")
    knn.fit(train, target)

    print("KNN - Prediciendo...")
    predictions = knn.predict(testVals)

    return predictions
