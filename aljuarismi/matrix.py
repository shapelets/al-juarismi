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


def find_best_n_discords(mt, parameters, m=None):
    """
    Execute the operation 'find best n discords' of Khiva.
    :param mt: The matrix profile and the index calculated previously.
    :param m: Subsequence length value used to calculate the matrix profile.
    :param parameters: The parameters of the function (number of clusters, ...).
    :return: Tuple with the discord distances, the discord indices and the subsequence indices.
    """
    (prof, ind) = mt

    n = parameters["n"]
    if not n:
        print('How many discords?')
        while not n:
            n = click.prompt('', type=int)
    data = kv.find_best_n_discords(prof, ind, m, n)
    return data[0].to_pandas(), data[1].to_pandas(), data[2].to_pandas()


def find_best_n_motifs(mt, parameters):
    """
    Execute the operation 'find best n motifs' of Khiva.
    :param mt: The matrix profile and the index calculated previously, and the m used.
    :param m: Subsequence length value used to calculate the matrix profile.
    :param parameters: The parameters of the function (number of clusters, ...).
    :return: Tuple with the motif distances, the motif indices and the subsequence indices.
    """
    (prof, ind) = mt
    n = parameters["n"]
    if not n:
        print('How many motifs?')
        while not n:
            n = click.prompt('', type=int)
    data = kv.find_best_n_motifs(prof, ind, m, n)
    return data[0].to_pandas(), data[1].to_pandas(), data[2].to_pandas()


def stomp(tt1, tt2, parameters):
    """
    Execute the 'stomp' of Khiva for two time series.
    :param tt1: First time series.
    :param tt2: Second time series.
    :param parameters: The parameters of the function (subsequence length, ...).
    :return: Tuple with profile and index.
    """
    tts1 = kv.Array(tt1)
    tts2 = kv.Array(tt2)
    sub_len = parameters["m"]
    if not sub_len:
        print('What is the length of the subsequence?')
        while not sub_len:
            sub_len = click.prompt('', type=int)
    data = kv.stomp(tts1, tts2, sub_len)
    stm = data[0].to_pandas()
    stm.set_axis(["profile"], axis='columns')
    stm["index"] = data[1].to_pandas()
    stm["m"] = pd.DataFrame([sub_len])
    return stm


def stomp_self_join(tt, parameters):
    """
    Execute the 'stomp' of Khiva for only one time series.
    :param tt: Time series.
    :param parameters: The parameters of the function (subsequence length, ...).
    :return: Tuple with profile and index
    """
    tts = kv.Array(tt)
    sub_len = parameters["m"]
    if not sub_len:
        print('What is the length of the subsequence?')
        while not sub_len:
            sub_len = click.prompt('', type=int)
    data = kv.stomp_self_join(tts, sub_len)
    stm = data[0].to_pandas().join(data[1].to_pandas())
    stm.set_axis(["profile", "index"], axis='columns')
    stm["m"] = pd.DataFrame([sub_len])
    return stm
