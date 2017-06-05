#!/usr/bin/python
# -*- coding: utf-8 -*-


from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

def getOutputScore(testIds, predictions) :
    
    dfTrips = pd.read_csv('../../DataSet/trip.csv')[['id', 'duration']]
    dfTrips.rename(columns={'duration':'real_duration'}, inplace=True)
    dfValidation = pd.DataFrame({'id':testIds, 'pred_duration':predictions})
    dfValidation = dfValidation.merge(dfTrips, how='inner', on='id')
    return mean_squared_error(dfValidation.real_duration, dfValidation.pred_duration)
