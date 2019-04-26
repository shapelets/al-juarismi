#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

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
    print('Current path is ' + os.getcwd())
    query = al.query_input()
    if query == 'here':
        path = os.getcwd()
    else:
        path = query
    return path


def load_dataset(parameters):
    """
    Load the dataset.
    :param parameters: The parameters which have the name of the dataset.
    """""
    dataset_name = parameters['Dataset']
    workspace = al.Workspace()

    data = workspace.get_dataset(dataset_name)
    if data is None:
        path = workspace.get_dataset_path(dataset_name)
        if path is None:
            path = ask_for_dataset_path()

        while not os.path.exists(path + '/' + dataset_name + '.csv'):
            print("Invalid path")
            print("Please introduce a valid one")
            path = ask_for_dataset_path()
        data = pd.read_csv(path + '/' + dataset_name + '.csv')
        workspace.save_dataset(dataset_name, data, path)

    workspace.save_dataset('current', data)


def create_dataset(parameters):
    """
    Creates a random dataset and saves it.
    :param parameters: The parameters for the creation (number of rows, numbers of columns,...).
    """
    workspace = al.Workspace()

    num_rows, num_col, values = rand_param(parameters)

    print('Creating the random dataset')
    al.voice('Creating the random dataset')

    tt = pd.DataFrame(index=range(num_rows))
    for n in range(num_col):
        tt['col' + str(n)] = pd.DataFrame(np.random.uniform(values[0], values[1], size=num_rows),
                                          dtype='float32')

    rand = workspace.get_counter('rand')
    workspace.save_dataset('random' + str(rand), tt)
    workspace.save_dataset('current', tt)
    print('Created and saved as random{} which has {} columns, {} rows and values '
          'between {} and {}'.format(str(rand), num_col, num_rows, values[0], values[1]))
    al.voice('Created and saved as random{} which has {} columns, {} rows and values '
             'between {} and {}'.format(str(rand), num_col, num_rows, values[0], values[1]))


def rand_param(parameters):
    """
    Obtains the parameters for the random dataset generator.
    :param parameters: The parameters for the creation (number of rows, numbers of columns,...).
    :return: A tuple of the parameters.
    """
    num_rows, num_col, values = 0, 0, []
    if parameters["columns"]:
        num_col = int(parameters["columns"])
    else:
        print('How many columns?')
        al.voice('How many columns?')
        query = al.query_input()
        while not query.isnumeric():
            print('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        num_col = int(query)

    if parameters["rows"]:
        num_rows = int(parameters["rows"])
    else:
        print('How many rows?')
        al.voice('How many rows?')
        query = al.query_input()
        while not query.isnumeric():
            print('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        num_rows = int(query)

    if parameters["values"]:
        values = parameters["values"]
    else:
        print('What is the minimum value?')
        al.voice('What is the minimum value?')
        query = al.query_input()
        while not al.isnumber(query):
            print('Incorrect input.\nIt is not a number.\nPlease introduce one:')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        values.append(float(query))
        print('And the maximum?')
        al.voice('And the maximum?')
        query = al.query_input()
        while not al.isnumber(query):
            print('Incorrect input.\nIt is not a number.\nPlease introduce one:')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        values.append(float(query))

    return num_rows, num_col, values


def get_subdataset_rows(parameters):
    """
    Obtains a subset of the dataset by its rows.
    :param parameters: The parameter of the function(dataset name,...).
    """
    workspace = al.Workspace()
    data_name = parameters['Dataset']
    dataset = workspace.get_dataset(data_name)

    if parameters["from"]:
        index_a = int(parameters["from"])
    else:
        print('From what row number?')
        al.voice('From what row number?')
        query = al.query_input()
        while not al.isnumber(query):
            print('Incorrect input.\nIt is not a number.\nPlease introduce one:')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        index_a = int(query)
    if parameters["to"]:
        index_b = int(parameters['to'])
    else:
        print('To what row number?')
        al.voice('To what row number?')
        query = al.query_input()
        while not al.isnumber(query):
            print('Incorrect input.\nIt is not a number.\nPlease introduce one:')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        index_b = int(query)

    dataset = dataset.iloc[index_a:index_b + 1]
    num = workspace.get_counter('sub')
    name = 'subrow' + str(num) + data_name
    workspace.save_dataset(name, dataset)
    txt = 'The sub-dataset by the rows is saved as ' + name
    print(txt)


def get_subdataset_columns(parameters):
    """
    Obtains a subset of the dataset by its columns.
    :param parameters: The parameter of the function(dataset name,...).
    """
    workspace = al.Workspace()
    data_name = parameters['Dataset']
    dataset = workspace.get_dataset(data_name)
    cols = []

    if parameters["cols"]:
        cols = parameters['cols']
    else:
        stop = False
        while not stop:
            cols.append(al.obtain_column(dataset))
            print('Do you want to continue? yes or no?')
            al.voice('Do you want to continue? yes or no?')
            response = al.query_input()
            if response == 'no':
                stop = True

    dataset = dataset[cols]
    num = workspace.get_counter('sub')
    name = 'subcol' + str(num) + data_name
    workspace.save_dataset(name, dataset)
    txt = 'The sub-dataset by the rows is saved as ' + name
    print(txt)
    al.voice(txt)
