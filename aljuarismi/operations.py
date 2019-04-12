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
    else:
        return

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

    if op == "stomp" and not parameters.get('Dataset2'):
        op = 'stomp_self_join'

    if op == "stomp":
        data_name = parameters["Dataset"]
        data_name2 = parameters["Dataset2"]
        dataset1 = workspace.get_dataset(data_name)
        dataset2 = workspace.get_dataset(data_name2)

        col = ''
        if dataset1.columns.size > 1:
            col = al.obtain_column(dataset1)
            dataset1 = dataset1[col]
        if dataset2.columns.size > 1:
            dataset2 = dataset2[al.obtain_column(dataset2)]

        (stomp, m) = al.stomp(dataset1.values, dataset2.values, parameters)
        number = workspace.get_counter('matrix_stomp')
        workspace.save_dataset('stomp' + str(number), stomp)
        workspace.save_dataset('m_stomp' + str(number), m)
        workspace.save_dataset('col_stomp' + str(number), col)
        print("The stomp is stored as stomp" + str(number))

    elif op == "stomp_self_join":
        data_name = parameters["Dataset"]
        dataset1 = workspace.get_dataset(data_name)

        col = ''
        if dataset1.columns.size > 1:
            col = al.obtain_column(dataset1)
            dataset1 = dataset1[col]

        (stomp, m) = al.stomp_self_join(dataset1.values, parameters)
        number = workspace.get_counter('matrix_stomp')
        workspace.save_dataset('stomp' + str(number), stomp)
        workspace.save_dataset('m_stomp' + str(number), m)
        workspace.save_dataset('col_stomp' + str(number), col)
        print("The stomp is stored as stomp" + str(number))

    elif op == "find_best_n_discords":
        if parameters.get('Dataset'):
            stomp_name = parameters['Dataset']
            stomp = workspace.get_dataset(stomp_name)
            m = workspace.get_dataset('m_' + stomp_name)
            col = workspace.get_dataset('col_' + stomp_name)
        else:
            num = workspace.get_last_number_counter('matrix_stomp')
            stomp = workspace.get_dataset('stomp' + str(num))
            m = workspace.get_dataset('m_stomp' + str(num))
            col = workspace.get_dataset('col_stomp' + str(num))

        discords = al.find_best_n_discords(stomp, m, parameters, col,
                                           workspace.get_dataset(parameters['originalDataset']))
        number = workspace.get_counter('matrix_best_d')
        workspace.save_dataset('discords' + str(number), discords)
        print('The best ' + str(int(parameters['n'])) + ' discord segments are stored as discord' + str(number))

    elif op == "find_best_n_motifs":
        if parameters.get('Dataset'):
            stomp_name = parameters['Dataset']
            stomp = workspace.get_dataset(stomp_name)
            m = workspace.get_dataset('m_' + stomp_name)
            col = workspace.get_dataset('col_' + stomp_name)
        else:
            num = workspace.get_last_number_counter('matrix_stomp')
            stomp = workspace.get_dataset('stomp' + str(num))
            m = workspace.get_dataset('m_stomp' + str(num))
            col = workspace.get_dataset('col_stomp' + str(num))

        motifs = al.find_best_n_motifs(stomp, m, parameters, col,
                                       workspace.get_dataset(parameters['originalDataset']))
        number = workspace.get_counter('matrix_best_m')
        workspace.save_dataset('motifs' + str(number), motifs)
        print('The best ' + str(int(parameters['n'])) + ' motifs segments are stored as motifs' + str(number))
