#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

import aljuarismi.utilities as ut


def exiting_yes(loaded_datasets, dataset_paths, response):
    print('Saving the workspace')
    datasets = list(loaded_datasets.keys())
    diff_datasets = list(filter(lambda x: x not in dataset_paths, datasets))
    for dataset in diff_datasets:
        f = open(dataset + ".csv", "w+")
        f.write(loaded_datasets[dataset])
        dataset_paths[dataset] = os.getcwd()
    ut.save_dictionary(dataset_paths)
    print('DEBUG: Fulfillment text: {}\n'.format(response))
    print('Closing program')
    exit()


def exiting_no(response):
    print('DEBUG: Fulfillment text: {}\n'.format(response))
    print('Closing program')
    exit()
