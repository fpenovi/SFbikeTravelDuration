#!/usr/bin/python
# -*- coding: utf-8 -*-

import RfPredictor
import Preprocessor
import csv


def main():
	train,target,testIds, testVals = Preprocessor.loadData('../../../DataSet/trip_train.csv',
														   '../../../DataSet/trip_test.csv')
	RfPredictor.predict(train, target, testIds, testVals)

if __name__ == "__main__":
    main()
