#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import matplotlib.pyplot as plt

import aljuarismi as al


def plot_dataset(dataset, parameters):
    """
    Plots graphically a column of the dataset.
    :param dataset: The current dataset.
    :param parameters: The parameter for the graphic.
    """
    a = int(parameters['from'] if parameters['from'] else 0)
    b = int(parameters['to'] if parameters['to'] else dataset.index.size)
    if b < a:
        print('This operation cannot be done.\nThe starting row number is greater than the last row number.')
        raise Exception()
    if b:
        dataset = dataset.iloc[:b]
    if a:
        dataset = dataset.iloc[a:]

    ncol = dataset.columns.size
    if ncol > 1:
        if not parameters["columns"]:
            column_name = al.obtain_column(dataset)
            plt.figure()
            plt.plot(dataset[column_name])
            plt.title(column_name)
            plt.show(block=False)
        else:
            for column_name in parameters["columns"]:
                plt.figure()
                plt.plot(dataset[column_name])
                plt.title(column_name)
                plt.show(block=False)

    else:
        plt.figure()
        plt.plot(dataset)
        plt.title(parameters["Dataset"])
        plt.show(block=False)


def execute_plot(parameters):
    """
    Execute the function plot.
    :param parameters: The parameters for the graphic (dataset name, intervals,...).
    """
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    dataset = workspace.get_dataset(data_name)
    plot_dataset(dataset, parameters)
