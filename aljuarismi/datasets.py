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

from aljuarismi import utilities as ut
from aljuarismi import workspace_manager as wsp


def ask_for_dataset_path():
    """
    Ask for the dataset path
    :return: The path introduced
    """
    print('Where is it located?')
    ut.voice('Where is it located?')
    query = ''
    while query == '' or query == 'here':
        query = click.prompt('')
    if query != 'here':
        path = query
    else:
        path = os.getcwd()
    return path


def load_dataset(dataset, path):
    """
    Load the dataset
    :param dataset: The name of the dataset to load
    :param path: The path where it is located the dataset to load
    :return: The loaded dataset
    """
    current_dataset = pd.read_csv(path + '/' + dataset + '.csv')
    wsp.create_instancer("workspace").set(dataset, current_dataset.to_json())
    return current_dataset


def execute_load_dataset(parameters):
    """
    Load the dataset
    :param parameters: The parameters which have the name of the dataset 
    :return: the loaded dataset
    """""
    dataset_paths = wsp.create_instancer("dataset_locator")
    loaded_datasets = wsp.create_instancer("workspace")
    dataset_name = parameters['Dataset']
    if dataset_name in loaded_datasets.getall():
        data = ut.obtain_dataset(loaded_datasets, dataset_name)
    else:
        if dataset_name in dataset_paths.getall():
            path = dataset_paths.get(dataset_name)
        else:
            path = ask_for_dataset_path()
            dataset_paths.set(dataset_name, path)
        data = load_dataset(dataset_name, path)
    return data


def create_dataset(parameters):
    """
    Creates a random dataset and saves it with the loaded ones
    :param parameters: The parameters
    :return: A random dataset
    """
    print('Creating the random dataset')
    ut.voice('Creating the random dataset')
    counters = wsp.create_instancer("counters")
    num_rand = counters.get("num_rand")
    tt = None
    if list(filter(lambda x: x == '' or [], list(parameters.values()))):
        tt = pd.DataFrame([rng.randrange(1, 100) for n in range(50)])
    else:
        pass

    wsp.create_instancer("workspace").set('random' + str(num_rand), tt.to_json())
    print("Created and saved as random" + str(num_rand))
    ut.voice("Created and saved as random" + str(num_rand))
    counters.set("num_rand", num_rand + 1)
    return tt
