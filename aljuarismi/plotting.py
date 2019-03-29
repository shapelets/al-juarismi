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

from aljuarismi import datasets as dt


def plot_dataset(dataset, parameters):
    """
    Plots graphically a column of the dataset
    :param dataset: The current dataset
    :param parameters: The parameter for the graphic
    :return:
    """
    name = ''
    ncol = dataset.columns.size
    if ncol - 1 > 1:
        if parameters["columns"] == []:
            print("I have more than one column available, which is the one to be selected?")
            print(list(dataset.columns.values))
            column_name = ''
            while column_name == '':
                column_name = click.prompt('Which column do you want to plot?', type=str)
                click.echo('DEBUG: %s' % column_name)
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
        plt.title('Series')
        plt.show(block=False)


def execute_plot(current_dataset, parameters):
    """
    Execute the function plot
    :param current_dataset: The current dataset
    :param parameters: The parameters for the graphic (dataset name, intervals,...)
    :return:
    """
    data_name = parameters["Dataset"]
    if data_name == '' or data_name == 'current_dataset':
        plot_dataset(current_dataset, parameters)
    else:
        dataset = dt.execute_load_dataset(parameters)
        plot_dataset(dataset, parameters)
