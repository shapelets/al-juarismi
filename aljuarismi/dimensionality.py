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


def reduce_datapoints(timeseries, parameters):
    """

    :param timeseries:
    :param num_points:
    :return:
    """
    if parameters.get("number") == '':
        print('How many point do you want to reduce it?')
        num_points = click.prompt('', type=int)
        click.echo('DEBUG: %d' % num_points)
    else:
        num_points = int(parameters.get("number"))

    k_array = kv.Array(timeseries)
    k_result_ = kv.paa(k_array, num_points)
    data = k_result_.to_pandas()
    return data
