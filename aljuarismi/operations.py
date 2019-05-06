#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import pandas as pd

import aljuarismi as al


def do_dimensionality(parameters):
    """
    Do an operation of dimensionality.
    :param parameters: The parameters of the function (name of the operation, ...).
    """

    op = parameters.pop("operation")
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    dataset = workspace.get_dataset(data_name)

    if op == "paa":
        # Calling khiva
        data = al.paa(dataset, parameters)
        num = workspace.get_counter('redux')
        workspace.save_dataset("paa" + str(num), data)
        print('The reduction of points is stored as paa' + str(num))

    elif op == 'pip':
        data = al.pip(dataset, parameters)
        num = workspace.get_counter('redux')
        workspace.save_dataset("pip" + str(num), data)
        print('The reduction of points is stored as pip' + str(num))

    elif op == 'ramer_douglas_peucker':
        data = al.ramer_douglas_peucker(dataset, parameters)
        num = workspace.get_counter('redux')
        workspace.save_dataset("RDP" + str(num), data)
        print('The reduction of points is stored as RDP' + str(num))

    elif op == 'visvalingam':
        data = al.visvalingam(dataset, parameters)
        num = workspace.get_counter('redux')
        workspace.save_dataset("visvalingam" + str(num), data)
        print('The reduction of points is stored as visvalingam' + str(num))


def do_clustering(parameters):
    """
    Do an operation of clustering.
    :param parameters: The parameters of the function (name of the operation, number of clusters, ...).
    """
    op = parameters.pop("operation")
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    dataset = workspace.get_dataset(data_name)

    if op == "kmeans":
        (centroids, labels) = al.kmean(dataset, parameters)
        number = workspace.get_counter('clustering')
        workspace.save_dataset('centroids' + str(number), centroids)
        workspace.save_dataset('labels' + str(number), labels)

    elif op == "kshape":
        (centroids, labels) = al.kshape(dataset, parameters)
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

        if dataset2 is None:
            if not data_name2 == "":
                print("The object " + data_name2 + " does not exist.")
                al.voice("The object " + data_name2 + " does not exist.")
            print("Please, provide the two datasets that should be stomped.")
            al.voice("Please, provide the two datasets that should be stomped.")
            return

        col = ''
        if dataset1.columns.size > 1:
            col = al.obtain_column(dataset1)
            dataset1 = dataset1[col]
        if dataset2.columns.size > 1:
            dataset2 = dataset2[al.obtain_column(dataset2)]

        (stomp, m) = al.stomp(dataset1.values, dataset2.values, parameters)
        number = workspace.get_counter('matrix_stomp')
        workspace.save_dataset('stomp' + str(number), (stomp.to_json(), m, col, dataset1.to_json()))
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
        workspace.save_dataset('stomp' + str(number), (stomp.to_json(), m, col, dataset1.to_json()))
        print("The stomp is stored as stomp" + str(number))

    elif op == "find_best_n_discords":
        stomp_name = parameters['Dataset']
        stomp = workspace.get_dataset(stomp_name)
        m, col, dataset = workspace.get_value(stomp_name)[1:]

        discords = al.find_best_n_discords(stomp, m, parameters, col, pd.read_json(dataset).sort_index())
        number = workspace.get_counter('matrix_best_d')
        workspace.save_dataset('discords' + str(number), discords)
        print('The best ' + str(int(parameters['n'])) + ' discord segments are stored as discords' + str(number))

    elif op == "find_best_n_motifs":
        stomp_name = parameters['Dataset']
        stomp = workspace.get_dataset(stomp_name)
        m, col, dataset = workspace.get_value(stomp_name)[1:]

        motifs = al.find_best_n_motifs(stomp, m, parameters, col, pd.read_json(dataset).sort_index())
        number = workspace.get_counter('matrix_best_m')
        workspace.save_dataset('motifs' + str(number), motifs)
        print('The best ' + str(int(parameters['n'])) + ' motifs segments are stored as motifs' + str(number))


def do_normalization(parameters):
    """
    Do an operation of normalization.
    :param parameters: The parameters of the function (name of the operation, dataset, ...).
    """
    op = parameters.pop("operation")
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    dataset = workspace.get_dataset(data_name)
    name = ''
    if not re.search("_in_place$", op):
        if op == 'decimal_scaling_norm':
            norm = al.decimal_scaling_norm(dataset)
            num_norm = str(workspace.get_counter('norm'))
            name = 'dec_sca_norm' + num_norm
            workspace.save_dataset(name, norm)

        elif op == 'max_min_norm':
            norm = al.max_min_norm(dataset, parameters)
            num_norm = str(workspace.get_counter('norm'))
            name = 'max_min_norm' + num_norm
            workspace.save_dataset(name, norm)

        elif op == 'mean_norm':
            norm = al.mean_norm(dataset)
            num_norm = str(workspace.get_counter('norm'))
            name = 'mean_norm' + num_norm
            workspace.save_dataset(name, norm)

        elif op == 'znorm':
            norm = al.znorm(dataset, parameters)
            num_norm = str(workspace.get_counter('norm'))
            name = 'znorm' + num_norm
            workspace.save_dataset(name, norm)

        print('The normalization is stored as ' + name)
        al.voice('The normalization is stored as ' + name)
    else:
        if op == 'decimal_scaling_norm_in_place':
            pass

        elif op == 'max_min_norm_in_place':
            pass

        elif op == 'mean_norm_in_place':
            pass

        elif op == 'znorm_in_place':
            pass


def get_library_backend(type):
    """
    Gets all backends.
    :param type: Type of backend (the current backend 'backend' or all the available backends 'backends')
    """
    if type == 'backend':
        al.get_backend()
    elif type == 'backends':
        al.get_backends()


def set_library_backend(parameters):
    """
    Set a backend.
    :param parameters: Parameter of the funtion (name of the backend,...).
    """
    type = parameters['library']
    backend = parameters['backend']
    if type == 'backend':
        al.set_backend(backend.upper())


def do_features(parameters):
    """
    Execute the feature operations.
    :param parameters: The parameters for this function (name_dataset).
    """
    workspace = al.Workspace()
    data_name = parameters['Dataset']
    dataset = workspace.get_dataset(data_name)
    features = al.features(dataset)
    num_norm = str(workspace.get_counter('feat'))
    name = data_name + 'Features' + num_norm
    workspace.save_dataset(name, features)

    print('The features are stored as ' + name)
    al.voice('The features are stored as ' + name)
