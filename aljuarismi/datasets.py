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
import numpy as np
import pandas as pd

import aljuarismi as al


def ask_for_dataset_path():
    """
    Ask for the dataset path
    :return: The path introduced
    """
    print('Where is it located?')
    al.voice('Where is it located?')
    query = ''
    while query == '' or query == 'here':
        query = click.prompt('')
    if query != 'here':
        path = query
    else:
        path = os.getcwd()
    return path


def execute_load_dataset(parameters):
    """
    Load the dataset
    :param parameters: The parameters which have the name of the dataset 
    :return: the loaded dataset
    """""
    dataset_name = parameters['Dataset']

    if dataset_name in al.Workspace().get_all_dataset():
        data = al.Workspace().get_dataset(dataset_name)
    else:
        if dataset_name in al.Workspace().get_all_dataset_paths():
            path = al.Workspace().get_dataset_path(dataset_name)
        else:
            path = ask_for_dataset_path()
        data = pd.read_csv(path + '/' + dataset_name + '.csv')
        al.Workspace().save_dataset(dataset_name, data, path)
    return data


def create_dataset(parameters):
    """
    Creates a random dataset and saves it with the loaded ones
    :param parameters: The parameters
    :return: A random dataset
    """
    print('Creating the random dataset')
    al.voice('Creating the random dataset')
    tt = None
    if list(filter(lambda x: x != '' or [], list(parameters.values()))) == [[]]:
        tt = pd.DataFrame([rng.randrange(1, 100) for n in range(50)])
    else:
        if parameters["columns"]:
            stack = np.array([rng.randrange(1, 100) for n in range(50)])
            for n in range(int(parameters["columns"]) - 1):
                rand = np.array([rng.randrange(1, 100) for n in range(50)])
                stack = np.vstack([stack, rand])
            tt = pd.DataFrame(stack)
    rand = al.Workspace().get_counter('rand')
    al.Workspace().save_dataset('random' + str(rand), tt)
    print("Created and saved as random" + str(rand))
    al.voice("Created and saved as random" + str(rand))
    return tt
