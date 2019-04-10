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
    data_name = parameters["Dataset"]
    dataset = workspace.get_dataset(data_name)

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
    data_name = parameters["Dataset"]
    dataset = workspace.get_dataset(data_name)

    if op == "kmeans":
        (centroids, labels) = al.kmean(dataset.values, parameters)
        number = workspace.get_counter('clustering')
        workspace.save_dataset('centroids' + str(number), centroids)
        workspace.save_dataset('labels' + str(number), labels)

    elif op == "kshape":
        (centroids, labels) = al.kshape(dataset.values, parameters)
        number = workspace.get_counter('clustering')
        workspace.save_dataset('centroids' + str(number), centroids)
        workspace.save_dataset('labels' + str(number), labels)

    print("The centroids are stored in centroids" + str(number))
    print("The labels are stored in labels" + str(number))


def do_matrix(parameters):
    """
    Do a operation of matrix.
    :param parameters: The parameters of the function (name of the operation, number of clusters, ...).
    :return:
    """
    op = parameters.pop("operation")
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    data_name2 = parameters["Dataset2"]
    dataset1 = workspace.get_dataset(data_name)
    dataset2 = workspace.get_dataset(data_name2)

    if op == "stomp" and data_name2 == '':
        op = 'stomp_self_join'

    if op == "stomp":
        if dataset1.columns.size > 1:
            dataset1 = dataset1[al.obtain_column(dataset1)]
        if dataset2.columns.size > 1:
            dataset2 = dataset2[al.obtain_column(dataset2)]
        stomp = al.stomp(dataset1.values, dataset2.values, parameters)
        number = workspace.get_counter('matrix_stomp')
        workspace.save_dataset('stomp' + str(number), stomp)
        print("The stomp is stored as stomp" + str(number))

    elif op == "stomp_self_join":
        if dataset1.columns.size > 1:
            dataset1 = dataset1[al.obtain_column(dataset1)]
        stomp = al.stomp_self_join(dataset1.values, parameters)
        number = workspace.get_counter('matrix_stomp')
        workspace.save_dataset('stomp' + str(number), stomp)
        print("The stomp is stored as stomp" + str(number))

    elif op == "find_best_n_discords":
        n = workspace.get_last_number_counter('stomp')
        stomp = workspace.get_dataset('stomp' + str(n))
        (distances, indexes, sub_ind) = al.find_best_n_discords(stomp, parameters)
        number = workspace.get_counter('matrix_best_d')
        workspace.save_dataset('distances' + str(number), distances)
        workspace.save_dataset('indexes' + str(number), indexes)
        workspace.save_dataset('subseq_index' + str(number), sub_ind)

    elif op == "find_best_n_motifs":
        n = workspace.get_last_number_counter('stomp')
        stomp = workspace.get_dataset('stomp' + str(n))
        (distances, indexes, sub_ind) = al.find_best_n_motifs(stomp, parameters)
        number = workspace.get_counter('matrix_best_m')
        workspace.save_dataset('distances' + str(number), distances)
        workspace.save_dataset('indexes' + str(number), indexes)
        workspace.save_dataset('subseq_index' + str(number), sub_ind)
