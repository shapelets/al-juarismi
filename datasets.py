import os

import click
import pandas as pd


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
