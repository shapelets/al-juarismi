#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import click
import khiva as kv


def kmean(tt, parameters):
    """
    Execute the kmeans of Khiva.
    :param parameters: The parameters of the function (number of clusters, ...).
    :param tt: The dataset which is computed.
    :return: Tuple with the centroids and labels.
    """
    tts = kv.Array(tt)
    k = parameters["number"]
    if not k:
        print('How many clusters?')
        while not k:
            k = click.prompt('', type=int)
    data = kv.k_means(tts, int(k))
    return data[0].to_pandas(), data[1].to_pandas()


def kshape(tt, parameters):
    """
    Execute the kshape of Khiva.
    :param parameters: The parameters of the function (number of clusters, ...).
    :param tt: The dataset which is computed.
    :return: Tuple with the centroids and labels.
    """
    tts = kv.Array(tt)
    k = parameters["number"]
    if not k:
        print('How many clusters?')
        while not k:
            k = click.prompt('', type=int)
    data = kv.k_shape(tts, int(k))
    return data[0].to_pandas(), data[1].to_pandas()
