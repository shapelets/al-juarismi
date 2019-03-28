#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import khiva as kv


def reduce_datapoints(timeseries, num_points):
    """

    :param timeseries:
    :param num_points:
    :return:
    """
    k_array = kv.Array(timeseries)
    k_result_ = kv.visvalingam(k_array, num_points)
    data = k_result_.to_pandas()
    return data
