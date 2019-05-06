#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re

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


def ask_for_dataset_extension(files):
    """
    Ask for the dataset extension file.
    :param files: All files with the same name.
    :return: The extension file.
    """
    print('What is the file extension (txt, csv)?')
    al.voice('What is the file extension (txt, csv)?')
    print('All the files that has been found with the same name: ' + str(files))
    return al.query_input()


def load_dataset(parameters):
    """
    Load the dataset.
    :param parameters: The parameters which have the name of the dataset.
    """""
    dataset_name = parameters['Dataset']
    extension = parameters['extension']
    workspace = al.Workspace()

    data = workspace.get_dataset(dataset_name)
    if data is None:
        path = workspace.get_dataset_path(dataset_name)

        if path is None:
            path = ask_for_dataset_path()
            while not os.path.exists(path):
                print('Invalid path.\nPlease introduce a valid one.')
                path = ask_for_dataset_path()

        if not extension:
            files = re.findall(dataset_name + '[^,\']*', str(os.listdir(path)))
            if len(files) == 0:
                raise Exception("There is no file with the name " + dataset_name +
                                ".\nPlease introduce a valid one the next time.")
            elif len(files) > 1:
                extension = ask_for_dataset_extension(files)
            else:
                extension = re.search('\..*', files[0]).group()[1:]

        abs_path = path + '/' + dataset_name + '.' + extension

        if not os.path.exists(abs_path):
            raise Exception("Invalid file.\nPlease introduce a valid one the next time.")
        if extension == 'csv':
            data = pd.read_csv(abs_path)
        elif extension == 'txt':
            data = pd.read_fwf(abs_path)
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

    if index_b < index_a:
        print('This operation cannot be done.\nThe starting row number is greater than the last row number.')
        raise Exception()

    dataset = dataset.iloc[index_a:index_b]
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


def change_name(parameters):
    """
    Change the name of an existing dataset.
    :param parameters: The parameter of the function (dataset name,...).
    """
    workspace = al.Workspace()
    or_name = parameters['Dataset']
    into_name = parameters['NameInto']
    if not into_name:
        print('Into what name do you want to change ' + or_name + '?')
        into_name = al.query_input()
    while into_name in workspace.get_all_dataset():
        print('There is already a dataset with the name ' + into_name + '.\nPlease write another name.')
        into_name = al.query_input()
    data = workspace.get_value(or_name)
    workspace.remove_dataset(or_name)
    workspace.save_dataset(into_name, data)
    print('The dataset named ' + or_name + ' has been updated into ' + into_name)


def join_by_cols(parameters):
    """
    Join two dataset with the same number of rows.
    :param parameters: The parameters of the function (dataset names).
    """
    workspace = al.Workspace()
    name_data1 = parameters['Dataset']
    name_data2 = parameters['Dataset2']
    dataset1 = workspace.get_dataset(name_data1)
    dataset2 = workspace.get_dataset(name_data2)

    if dataset2 is None:
        if not name_data2 == "":
            print("The object " + name_data2 + " does not exist.")
            al.voice("The object " + name_data2 + " does not exist.")
        print("Please, provide the two datasets that should be joined.")
        al.voice("Please, provide the two datasets that should be joined.")
        return

    if dataset1.index.size != dataset2.index.size:
        print('Not able to execute.\nThe datasets have different number of rows')
        return

    dataset = dataset1.join(dataset2, rsuffix='_0')
    num = workspace.get_counter('join')
    name = 'join' + str(num)
    workspace.save_dataset(name, dataset)
    print('The resulting dataset between ' + name_data1 + ' and ' + name_data2 + ' is saved as ' + name)


def split_by_cols(parameters):
    """
    Split a dataset into n datasets of m columns.
    :param parameters: The parameters of the function (dataset name, size of the split dataset for the column).
    """
    workspace = al.Workspace()
    name_data = parameters['Dataset']
    dataset = workspace.get_dataset(name_data)

    if parameters['split']:
        div = int(parameters['split'])
    else:
        print('How many cols will each dataset have?')
        al.voice('How many cols will each dataset have?')
        query = al.query_input()
        while not al.isnumber(query):
            print('Incorrect input.\nIt is not a number.\nPlease introduce one:')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        div = int(query)

    it = 0
    names = []
    while it < dataset.columns.size:
        div_dataset = dataset.iloc[:, it:it + div]
        num = workspace.get_counter('split')
        name = name_data + 'c' + str(num)
        names.append(name)
        workspace.save_dataset(name, div_dataset)
        it = it + div

    print('The splits of ' + name_data + ' are saved as: ' + str(names)[1:-1])


def join_by_rows(parameters):
    """
    Join two dataset with the same number of columns.
    :param parameters: The parameters of the function (dataset names).
    """
    workspace = al.Workspace()
    name_data1 = parameters['Dataset']
    name_data2 = parameters['Dataset2']
    dataset1 = workspace.get_dataset(name_data1)
    dataset2 = workspace.get_dataset(name_data2)

    if dataset2 is None:
        if not name_data2 == "":
            print("The object " + name_data2 + " does not exist.")
            al.voice("The object " + name_data2 + " does not exist.")
        print("Please, provide the two datasets that should be joined.")
        al.voice("Please, provide the two datasets that should be joined.")
        return

    if dataset1.columns.size != dataset2.columns.size:
        print('Not able to execute.\nThe datasets have different number of columns')
        return

    dataset = pd.concat([dataset1, dataset2], ignore_index=True)
    num = workspace.get_counter('join')
    name = 'join' + str(num)
    workspace.save_dataset(name, dataset)
    print('The resulting dataset between ' + name_data1 + ' and ' + name_data2 + ' is saved as ' + name)


def split_by_rows(parameters):
    """
    Split a dataset into n datasets of m rows.
    :param parameters: The parameters of the function (dataset name, size of the split dataset for the rows).
    """
    workspace = al.Workspace()
    name_data = parameters['Dataset']
    dataset = workspace.get_dataset(name_data)

    if parameters['split']:
        div = int(parameters['split'])
    else:
        print('How many rows will each dataset have?')
        al.voice('How many rows will each dataset have?')
        query = al.query_input()
        while not al.isnumber(query):
            print('Incorrect input.\nIt is not a number.\nPlease introduce one:')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        div = int(query)

    it = 0
    names = []
    while it < dataset.index.size:
        div_dataset = dataset.iloc[it:it + div]
        num = workspace.get_counter('split')
        name = name_data + 'r' + str(num)
        names.append(name)
        workspace.save_dataset(name, div_dataset)
        it = it + div

    print('The splits of ' + name_data + ' are saved as: ' + str(names)[1:-1])
