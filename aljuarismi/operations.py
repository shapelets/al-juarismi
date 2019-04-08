#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import aljuarismi as al


def do_op(parameters):
    """
    Do a operation of dimensionality.
    :param parameters: The parameters of the function (name of the operation, ...).
    :return:
    """

    op = parameters.pop("Operations")
    workspace = al.Workspace()
    dataset = workspace.get_dataset('current')
    if op == "reduction_points":
        # Calling khiva
        c = workspace.get_counter('redux')
        data = al.reduce_datapoints(dataset.values, parameters)
        workspace.save_dataset("redux" + str(c), data)

        print('The reduction of points is stored as redux' + str(c))


def do_clustering(parameters):
    """
    Do a operation of clustering.
    :param parameters: The parameters of the function (name of the operation, number of clusters, ...).
    :return:
    """
    op = parameters.pop("operation")
    workspace = al.Workspace()
    dataset = workspace.get_dataset('current')
    data_name = parameters["Dataset"]
    if data_name:
        dataset = workspace.get_dataset(data_name)
        if dataset is None:
            return

    if op == "kmeans":
        (centroids, labels) = al.kmean(dataset.values, parameters)
        number = workspace.get_counter('var')
        al.Workspace().save_dataset('centroids' + str(number), centroids)
        al.Workspace().save_dataset('labels' + str(number), labels)

    elif op == "kshape":
        (centroids, labels) = al.kshape(dataset.values, parameters)
        number = workspace.get_counter('var')
        al.Workspace().save_dataset('centroids' + str(number), centroids)
        al.Workspace().save_dataset('labels' + str(number), labels)

    print("The centroids are stored in centroids" + str(number))
    print("The labels are stored in labels" + str(number))
