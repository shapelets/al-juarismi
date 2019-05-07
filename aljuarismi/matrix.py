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
import pandas as pd


def find_best_n_discords(mt, m, parameters, col, dataset):
    """
    Execute the operation 'find best n discords' of Khiva.
    :param mt: The matrix profile and the index calculated previously.
    :param m: Subsequence length value used to calculate the matrix profile.
    :param parameters: The parameters of the function (number of clusters, ...).
    :param col: The column which has been used in stomp.
    :param dataset: The (first) dataset which has been used in stomp.
    :return: Dataframe with the discord distances, the discord indices and the subsequence indices.
    """
    prof = kv.Array(mt.get("profile").to_list(), khiva_type=kv.dtype.f32)
    ind = kv.Array(mt.get("index").to_list(), khiva_type=kv.dtype.u32)
    n = parameters["n"]
    if not n:
        print('How many discords?')
        while not n:
            n = click.prompt('', type=int)
    n = int(n)
    distance, index, subsequence = kv.find_best_n_discords(prof, ind, m, n)
    stm = pd.DataFrame(index=range(m))
    sub = subsequence.to_numpy()
    if col:
        dataset = dataset[col]
    if n == 1:
        aux = dataset[sub.min():sub.min() + m]
        aux.index = range(m)
        stm["col" + str(0)] = aux
    else:
        for it in range(n):
            aux = dataset[sub[it]:sub[it] + m]
            aux.index = range(m)
            stm["col" + str(it)] = aux
    return stm


def find_best_n_motifs(mt, m, parameters, col, dataset):
    """
    Execute the operation 'find best n motifs' of Khiva.
    :param mt: The matrix profile and the index calculated previously, and the m used.
    :param m: Subsequence length value used to calculate the matrix profile.
    :param parameters: The parameters of the function (number of clusters, ...).
    :param col: The column which has been used in stomp.
    :param dataset: The (first) dataset which has been used in stomp.
    :return: Tuple with the motif distances, the motif indices and the subsequence indices.
    """
    prof = kv.Array(mt.get("profile").to_list(), khiva_type=kv.dtype.f32)
    ind = kv.Array(mt.get("index").to_list(), khiva_type=kv.dtype.u32)
    n = parameters["n"]
    if not n:
        print('How many motifs?')
        while not n:
            n = click.prompt('', type=int)
    n = int(n)
    distance, index, subsequence = kv.find_best_n_motifs(prof, ind, m, n)
    stm = pd.DataFrame(index=range(m))
    sub = subsequence.to_numpy()
    if col:
        dataset = dataset[col]
    if n == 1:
        aux = dataset[sub.min():sub.min() + m]
        aux.index = range(m)
        stm["col" + str(0)] = aux
    else:
        for it in range(n):
            aux = dataset[sub[it]:sub[it] + m]
            aux.index = range(m)
            stm["col" + str(it)] = aux
    return stm


def stomp(tt1, tt2, parameters):
    """
    Execute the 'stomp' of Khiva for two time series.
    :param tt1: First time series.
    :param tt2: Second time series.
    :param parameters: The parameters of the function (subsequence length, ...).
    :return: Tuple with a dataframe with profile and index matrix, and the subsequence length (m).
    """
    tts1 = kv.Array(tt1)
    tts2 = kv.Array(tt2)
    sub_len = parameters["m"]
    if not sub_len:
        print('What is the length of the subsequence?')
        while not sub_len:
            sub_len = click.prompt('', type=int)
    sub_len = int(sub_len)
    data = kv.stomp(tts1, tts2, sub_len)
    stm = data[0].to_pandas()
    stm.set_axis(["profile"], axis='columns')
    stm["index"] = data[1].to_pandas()

    return stm, sub_len


def stomp_self_join(tt, parameters):
    """
    Execute the 'stomp' of Khiva for only one time series.
    :param tt: Time series.
    :param parameters: The parameters of the function (subsequence length, ...).
    :return: Tuple with a dataframe with profile and index matrix, and the subsequence length (m).
    """
    tts = kv.Array(tt)
    sub_len = parameters["m"]
    if not sub_len:
        print('What is the length of the subsequence?')
        while not sub_len:
            sub_len = click.prompt('', type=int)
    sub_len = int(sub_len)
    data = kv.stomp_self_join(tts, sub_len)
    stm = data[0].to_pandas()
    stm.set_axis(["profile"], axis='columns')
    stm["index"] = data[1].to_pandas()
    return stm, sub_len
