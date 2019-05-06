#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from khiva import normalization as nm


def __add_parameters(parameters):
    """
    Adds the parameters for the function
    :param parameters: parameter of the function
    :return: string of part of thr parameters
    """
    param = ''
    if parameters['max']:
        param = param + ', high = ' + str(parameters['max'])
    if parameters['min']:
        param = param + ', low = ' + str(parameters['min'])
    if parameters['epsilon']:
        param = param + ', epsilon = ' + str(parameters['epsilon'])

    return param


def znorm(dataset, parameters):
    """
    Execute the znorm of Khiva.
    :return: Tuple with the centroids and labels.
    :param dataset: The dataset which is computed.
    :param parameters: The parameters of the function (epsilon).
    :return: The normalization of the dataset.
    """
    tt = nm.Array(dataset)
    func = 'nm.znorm(tt' + __add_parameters(parameters) + ').to_pandas()'
    result = eval(func)
    ncol = dataset.columns.size
    index = list(map(lambda a: 'col' + str(a), list(range(ncol))))
    result.set_axis(index, axis='columns', inplace=True)
    return result


def max_min_norm(dataset, parameters):
    """
    Execute the max min norm of Khiva.
    :return: Tuple with the centroids and labels.
    :param dataset: The dataset which is computed.
    :param parameters: The parameters of the function (high, low, epsilon).
    :return: The normalization of the dataset.
    """
    tt = nm.Array(dataset)
    func = 'nm.max_min_norm(tt' + __add_parameters(parameters) + ').to_pandas()'
    result = eval(func)
    ncol = dataset.columns.size
    index = list(map(lambda a: 'col' + str(a), list(range(ncol))))
    result.set_axis(index, axis='columns', inplace=True)
    return result


def mean_norm(dataset):
    """
    Execute the mean norm of Khiva.
    :return: Tuple with the centroids and labels.
    :param dataset: The dataset which is computed.
    :return: The normalization of the dataset.
    """
    tt = nm.Array(dataset)
    result = nm.mean_norm(tt).to_pandas()
    ncol = dataset.columns.size
    index = list(map(lambda a: 'col' + str(a), list(range(ncol))))
    result.set_axis(index, axis='columns', inplace=True)
    return result


def decimal_scaling_norm(dataset):
    """
    Execute the decimal scaling norm of Khiva.
    :return: Tuple with the centroids and labels.
    :param dataset: The dataset which is computed.
    :return: The normalization of the dataset.
    """
    tt = nm.Array(dataset)
    result = nm.decimal_scaling_norm(tt).to_pandas()
    ncol = dataset.columns.size
    index = list(map(lambda a: 'col' + str(a), list(range(ncol))))
    result.set_axis(index, axis='columns', inplace=True)
    return result
