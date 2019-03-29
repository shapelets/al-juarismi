#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import string

import pandas as pd


def id_session_creator():
    """
    Creates the random string which will be use in the session_id
    :return: The random string
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def obtain_dataset(database, dataset):
    """
    Finds in the database and converts the dataset from json to pandas
    :param database: The database where it is located
    :param dataset: The name of the dataset to find
    :return: The dataset as a pandas
    """
    ds_json = database.get(dataset)
    return pd.read_json(ds_json)
