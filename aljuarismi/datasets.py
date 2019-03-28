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

from aljuarismi import workspace_manager as wsp


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
    loaded_datasets.set(dataset, current_dataset)
    return current_dataset


def execute_load_dataset(parameters, loaded_datasets):
    """
    Load the dataset
    :param parameters: The parameters which have the name of the dataset 
    :param loaded_datasets: The already loaded dataset
    :return: the loaded dataset
    """""
    dataset_paths = wsp.create_instancer("dataset_locator")
    dataset_name = parameters['Dataset']
    if dataset_name in loaded_datasets.getall():
        data = loaded_datasets[dataset_name]
    else:
        if dataset_name in dataset_paths.getall():
            path = dataset_paths.get(dataset_name)
        else:
            path = ask_for_dataset_path()
            dataset_paths.set(dataset_name, path)
        data = load_dataset(loaded_datasets, dataset_name, path)
    return data


def create_dataset(parameters, loaded_datasets):
    """
    Creates a random dataset and saves it with the loaded ones
    :param parameters: The parameters
    :param loaded_datasets: The already loaded dataset
    :return: A random dataset
    """
    counters = wsp.create_instancer("counters")
    num_rand = counters.get("num_rand")
    tt = pd.DataFrame([rng.randrange(1, 100) for n in range(50)])
    loaded_datasets.set('random' + str(num_rand), tt)
    counters.set("num_rand", num_rand + 1)
    return tt

