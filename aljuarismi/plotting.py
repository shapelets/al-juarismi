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


def plot_dataset(dataset):
    """
    Plots graphically a column of the dataset
    :param dataset: the current dataset
    :return:
    """
    name = ''
    ncol = dataset.columns.size
    if ncol - 1 > 1:
        print("I have more than one column available, which is the one to be selected?")
        print(list(dataset.columns.values))
        column_name = ''
        while column_name == '':
            column_name = click.prompt('Which column do you want to plot?', type=str)
            click.echo('DEBUG: %s' % column_name)

    plt.figure()
    plt.plot(dataset[column_name])
    plt.title(column_name)
    plt.show(block=False)


def execute_plot(current_dataset):
    """
    Execute the function plot
    :param current_dataset: the current dataset
    :return:
    """
    plot_dataset(current_dataset)
