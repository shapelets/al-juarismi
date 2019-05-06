#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import khiva as kv
import numpy as np
import pandas as pd


def features(dataset):
    """
    Execute some operations of features.
    :param dataset: The dataset which is computed.
    :return: A pandas which has all the results.
    """
    arr_tmp = kv.Array(dataset.transpose())
    features = np.stack([kv.abs_energy(arr_tmp).to_numpy(),
                         kv.absolute_sum_of_changes(arr_tmp).to_numpy(),
                         kv.count_above_mean(arr_tmp).to_numpy(),
                         kv.count_below_mean(arr_tmp).to_numpy(),
                         kv.first_location_of_maximum(arr_tmp).to_numpy(),
                         kv.first_location_of_minimum(arr_tmp).to_numpy(),
                         kv.has_duplicates(arr_tmp).to_numpy(),
                         kv.has_duplicate_max(arr_tmp).to_numpy(),
                         kv.kurtosis(arr_tmp).to_numpy(),
                         kv.last_location_of_maximum(arr_tmp).to_numpy(),
                         kv.last_location_of_minimum(arr_tmp).to_numpy(),
                         kv.has_duplicate_min(arr_tmp).to_numpy(),
                         kv.longest_strike_above_mean(arr_tmp).to_numpy(),
                         kv.longest_strike_below_mean(arr_tmp).to_numpy(),
                         kv.maximum(arr_tmp).to_numpy(),
                         kv.mean_absolute_change(arr_tmp).to_numpy(),
                         kv.minimum(arr_tmp).to_numpy(),
                         kv.number_crossing_m(arr_tmp, 0).to_numpy(),
                         kv.mean(arr_tmp).to_numpy(),
                         kv.median(arr_tmp).to_numpy(),
                         kv.mean_change(arr_tmp).to_numpy(),
                         kv.ratio_value_number_to_time_series_length(arr_tmp).to_numpy(),
                         kv.skewness(arr_tmp).to_numpy(),
                         kv.standard_deviation(arr_tmp).to_numpy(),
                         kv.sum_of_reoccurring_values(arr_tmp).to_numpy(),
                         kv.sum_values(arr_tmp).to_numpy(),
                         kv.variance(arr_tmp).to_numpy(),
                         kv.variance_larger_than_standard_deviation(arr_tmp).to_numpy()])

    return pd.DataFrame(features)
