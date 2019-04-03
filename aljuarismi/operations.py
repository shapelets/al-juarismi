#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import aljuarismi as al


def do_op(parameters, dataset):
    # Workspace().set("redux", data)

    op = parameters.pop("Operations")
    if op == "reduction_points":
        # Calling khiva
        c = al.Workspace().get_counter('redux')
        data = al.reduce_datapoints(dataset.values, parameters)
        al.Workspace().save_dataset("redux" + str(c), data)

        print('The reduction of points is stored as redux' + str(c))


def do_clustering(parameters, dataset):
    op = parameters.pop("operation")
    if parameters["Dataset"]:
        dataset = al.Workspace().get_dataset(parameters["Dataset"])

    if op == "kmeans":
        data = al.kmean(dataset.values, parameters)
        var = al.Workspace().get_counter('var')
        al.Workspace().save_dataset('var' + str(var), data)

    elif op == "kshape":
        data = al.kshape(dataset.values, parameters)
        var = al.Workspace().get_counter('var')
        al.Workspace().save_dataset('var' + str(var), data)

    print("It is stored as var" + str(var))
