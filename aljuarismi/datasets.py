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


def ask_for_dataset_path():
    """
    Ask for the dataset path
    :return: The path introduced
    """
    print('Where is it located?')
    query = ''
    while query == '' or query == 'here':
        query = click.prompt('')
    if query != 'here':
        path = query
    else:
        path = os.getcwd()
    return path


def load_dataset(loaded_datasets, dataset, path):
    """
    Load the dataset
    :param loaded_datasets: The already loaded datsets
    :param dataset: The name of the dataset to load
    :param path: The path where it is located the dataset to load
    :return: The loaded dataset
    """
    current_dataset = pd.read_csv(path + '/' + dataset + '.csv')
    loaded_datasets[dataset] = current_dataset
    return current_dataset


def execute_load_dataset(parameters, loaded_datasets, dataset_paths):
    """
    Load the dataset
    :param parameters: The parameters which have the name of the dataset 
    :param loaded_datasets: The already loaded dataset
    :param dataset_paths: The path of the datasets which have been loaded previously in this session or another
    :return: the loaded dataset
    """""
    dataset_name = parameters['Dataset']
    if dataset_name in loaded_datasets.keys():
        data = loaded_datasets[dataset_name]
    else:
        if dataset_name in dataset_paths.keys():
            path = dataset_paths[dataset_name]
        else:
            path = ask_for_dataset_path()
            dataset_paths[dataset_name] = path
        data = load_dataset(loaded_datasets, dataset_name, path)
    return data


def createDataset(parameters, loaded_datasets):
    """
    Creates a random dataset and saves it with the loaded ones
    :param parameters: The parameters
    :param loaded_datasets: The already loaded dataset
    :return: A random dataset
    """
    tt = pd.DataFrame([rng.randrange for n in range(50)])
    loaded_datasets['random' + str(num_rand)] = tt
    return tt
