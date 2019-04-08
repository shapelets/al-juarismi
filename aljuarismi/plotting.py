#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import click
import matplotlib.pyplot as plt

import aljuarismi as al


def plot_dataset(dataset, parameters):
    """
    Plots graphically a column of the dataset.
    :param dataset: The current dataset.
    :param parameters: The parameter for the graphic.
    :return:
    """
    ncol = dataset.columns.size
    if ncol - 1 > 1:
        if not parameters["columns"]:
            print("I have more than one column available, which is the one to be selected?")
            al.voice("I have more than one column available, which is the one to be selected?")
            print(list(dataset.columns.values))
            column_name = ''
            while column_name not in list(dataset.columns.values):
                al.voice('Which column do you want to plot?')
                column_name = click.prompt('Which column do you want to plot?', type=str)
                click.echo('DEBUG: %s' % column_name)
                if column_name not in list(dataset.columns.values):
                    print('Incorrect column')
                    al.voice('Incorrect column')

            plt.figure()
            plt.plot(dataset[column_name].values)
            plt.title(column_name)
            plt.show(block=False)
        else:
            for column_name in parameters["columns"]:
                plt.figure()
                plt.plot(dataset[column_name].values)
                plt.title(column_name)
                plt.show(block=False)

    else:
        plt.figure()
        plt.plot(dataset.values)
        plt.title(parameters["Dataset"])
        plt.show(block=False)


def execute_plot(dataset, parameters):
    """
    Execute the function plot.
    :param dataset: The current dataset.
    :param parameters: The parameters for the graphic (dataset name, intervals,...).
    :return:
    """
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    if data_name:
        dataset = workspace.get_dataset(data_name)
        if dataset is None:
            return
    plot_dataset(dataset, parameters)
