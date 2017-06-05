#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.neighbors import KNeighborsRegressor
import csv
import sys
import src.utils as utils

DISTANCES = {-2:'braycurtis', -1:'canberra', 0:'hamming', 1:'manhattan', 2:'euclidean'}

def predict(train, target, testIds, testVals, neighbors, distance=2):

    m_distance = DISTANCES[distance] if (distance in DISTANCES) else 'minkowski'
    p_distance = distance if (m_distance not in DISTANCES) else None

    knn = KNeighborsRegressor(n_neighbors=neighbors, weights='distance',
                              algorithm='kd_tree', leaf_size=30, p=p_distance,
                              metric=m_distance, metric_params=None, n_jobs=-1)     # Jobs = -1 elije numero de
                                                                                    # jobs segun cantidad de cores.
    print("Volcando puntos...")
    knn.fit(train, target)

    print("Prediciendo...")
    predictions = knn.predict(testVals)

    return predictions

def exportResults(predictions, testIds, filename) :

    print("Guardando a archivo...")

    with open(filename, utils.getSystemWriteMode()) as outfile:
        rows = [["id", "duration"]]

        for idTest, prediction in zip(testIds, predictions):
            rows.append([idTest, prediction])

        out_csv = csv.writer(outfile)
        out_csv.writerows(rows)

    print("Se guardó a " + filename + " exitosamente")
