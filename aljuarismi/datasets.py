#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import random as rng

import click
import pandas as pd

num_rand = 0


def askForDatasetPath():
    print('Where is it located?')
    query = ''
    while query == '' or query == 'here':
        query = click.prompt('')
    if query != 'here':
        path = query
    else:
        path = os.getcwd()
    return path


def loadDataset(loadedDatasets, dataset, path):
    current_dataset = pd.read_csv(path + '/' + dataset + '.csv')
    loadedDatasets[dataset] = current_dataset
    return current_dataset


def executeLoadDataset(parameters, loadedDatasets, datasetPaths):
    """Load the dataset"""
    dataset_name = parameters['Dataset']
    if dataset_name in loadedDatasets.keys():
        data = loadedDatasets[dataset_name]
    else:
        if dataset_name in datasetPaths.keys():
            path = datasetPaths[dataset_name]
        else:
            path = askForDatasetPath()
            datasetPaths[dataset_name] = path
        data = loadDataset(loadedDatasets, dataset_name, path)
    return data


def createDataset(parameters, loadedDatasets):
    tt = pd.DataFrame([rng.randrange for n in range(50)])
    loadedDatasets['random' + num_rand] = tt
    return tt
