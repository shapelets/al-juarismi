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
    Ask for the dataset path.
    :return: The path introduced.
    """
    print('Where is it located?')
    al.voice('Where is it located?')
    print('Actual path is ' + os.getcwd())
    query = ''
    while query == '':
        query = click.prompt('')
    if query == 'here':
        path = os.getcwd()
    else:
        path = query
    return path


def load_dataset(parameters):
    """
    Load the dataset.
    :param parameters: The parameters which have the name of the dataset.
    :return: The loaded dataset.
    """""
    dataset_name = parameters['Dataset']

    if dataset_name in al.Workspace().get_all_dataset():
        data = al.Workspace().get_dataset(dataset_name)
    else:
        if dataset_name in al.Workspace().get_all_dataset_paths():
            path = al.Workspace().get_dataset_path(dataset_name)
        else:
            path = ask_for_dataset_path()

        while not os.path.exists(path + '/' + dataset_name + '.csv'):
            print("Invalid path")
            print("Please introduce a valid one")
            path = ask_for_dataset_path()
        data = pd.read_csv(path + '/' + dataset_name + '.csv')
        al.Workspace().save_dataset(dataset_name, data, path)
    return data


def create_dataset(parameters):
    """
    Creates a random dataset and saves it.
    :param parameters: The parameters for the creation (number of rows, numbers of columns,...).
    :return: A random dataset.
    """
    print('Creating the random dataset')
    al.voice('Creating the random dataset')
    if list(filter(lambda x: x != '' or [], list(parameters.values()))) == [[]]:
        tt = pd.DataFrame([rng.randrange(1, 100) for n in range(50)])
    else:
        num_rows, num_col, values = 50, 1, [0, 100]
        if parameters["columns"]:
            num_col = int(parameters["columns"])
        if parameters["rows"]:
            num_rows = int(parameters["rows"])
        if parameters["values"]:
            values = parameters["values"]

        tt = pd.DataFrame(index=range(num_rows))
        for n in range(num_col):
            tt['col' + str(n)] = pd.DataFrame(np.random.random_integers(values[0], values[1], num_rows),
                                              dtype='float32')
    rand = al.Workspace().get_counter('rand')
    al.Workspace().save_dataset('random' + str(rand), tt)
    print("Created and saved as random" + str(rand))
    al.voice("Created and saved as random" + str(rand))
    return tt
