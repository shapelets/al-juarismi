#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import khiva as kv

import aljuarismi as al


def get_int_number(parameters):
    """
    Obtains or asks for a integer number.
    :param parameters: the parameters of the function(number,...).
    :return: An integer number.
    """
    if parameters["number"]:
        num_points = int(parameters["number"])
    else:
        print('How many point do you want to reduce it?')
        al.voice('How many point do you want to reduce it?')
        query = al.query_input()
        while not query.isnumeric():
            print('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        num_points = int(query)
    return num_points


def get_epsilon(parameters):
    """
    Obtains or asks for the epsilon.
    :param parameters: the parameters of the function(number,...).
    :return: The epsilon value.
    """
    # Although we are asking for the epsilon, the value it is saved in the key number
    if parameters["number"]:
        num_points = parameters["number"]
    else:
        print('What is the value of epsilon?')
        al.voice('What is the value of epsilon?')
        query = al.query_input()
        while not query.isnumeric():
            print('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            al.voice('Incorrect input.\nIt is not a number.\nPlease introduce one.')
            query = al.query_input()
        num_points = float(query)
    return num_points


def paa(dataset, parameters):
    """
    Executes the function paa of khiva.
    :param dataset: The dataset which is computed.
    :param parameters: The parameters of the function (number of points).
    :return: The timeserie with the reduced points.
    """

    num_points = al.get_int_number(parameters)
    if dataset.columns.size > 1:
        dataset = dataset[al.obtain_column(dataset)]
    k_array = kv.Array(dataset)
    result = kv.paa(k_array, num_points)
    return result.to_pandas()


def pip(dataset, parameters):
    """
    Executes the function pip of khiva.
    :param dataset: The dataset which is computed.
    :param parameters: The parameters of the function (number of pip).
    :return: The timeserie with the reduced points.
    """
    num_pip = al.get_int_number(parameters)
    if dataset.columns.size > 1:
        dataset = dataset[al.obtain_column(dataset)]
    k_array = kv.Array([range(dataset.size), dataset.to_numpy().flatten()])
    result = kv.pip(k_array, num_pip).transpose()
    result = result.to_pandas()
    result.set_index(0, inplace=True)
    result.set_index(result.index.astype('int32'), inplace=True)
    return result


def ramer_douglas_peucker(dataset, parameters):
    """
    Executes the function Ramer-Douglas-Peucker of khiva.
    :param dataset: The dataset which is computed.
    :param parameters: The parameters of the function (epsilon).
    :return: The timeserie with the reduced points.
    """
    epsilon = al.get_float_number(parameters)
    if dataset.columns.size > 1:
        dataset = dataset[al.obtain_column(dataset)]
    k_array = kv.Array([range(dataset.size), dataset.to_numpy().flatten()])
    result = kv.ramer_douglas_peucker(k_array, epsilon).transpose()
    result = result.to_pandas()
    result.set_index(0, inplace=True)
    result.set_index(result.index.astype('int32'), inplace=True)
    return result


def visvalingam(dataset, parameters):
    """
    Executes the function Visvalingam of khiva.
    :param dataset: The dataset which is computed.
    :param parameters: The parameters of the function (number of points).
    :return: The timeserie with the reduced points.
    """
    num_pip = al.get_int_number(parameters)
    if dataset.columns.size > 1:
        dataset = dataset[al.obtain_column(dataset)]
    k_array = kv.Array([range(dataset.size), dataset.to_numpy().flatten()])
    result = kv.pip(k_array, num_pip).transpose()
    result = result.to_pandas()
    result.set_index(0, inplace=True)
    result.set_index(result.index.astype('int32'), inplace=True)
    return result


