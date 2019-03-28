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


def id_session_creator():
    """
    Creates the random string which will be use in the session_id
    :return: The random string
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def save_dictionary(dataset_paths):
    """
    Saves in a file the dataset file names and paths we had loaded in the previous or actual session
    :return:
    """
    f = open("./resources/DictionaryDataset.txt", "w+")
    for key, val in dataset_paths.items():
        f.write(key + ',' + val + '\n')
    f.close()


def load_dictionary():
    """
    Load the file which contains the names and paths of the datasets that had been loaded in previous sessions
    :return:
    """
    f = open("./resources/DictionaryDataset.txt", "r")
    paths = {}
    for line in f:
        fields = line.split(",")
        paths[fields[0]] = fields[1].rstrip()
    f.close()
    return paths
