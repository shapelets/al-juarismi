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
    ncol = dataset.count()
    if ncol - 1 > 1:
        print("Which column do you want to print?")
        query = ''
        while query != '':
            click.prompt('')
        if query.isdigit():
            aux = list(dataset.columns.values)
            name = aux.pop(int(query))
        else:
            name = query
    plt.plot(dataset[name])
    plt.show()


def execute_plot(current_dataset):
    """
    Execute the function plot
    :param current_dataset: the current dataset
    :return:
    """
    plot_dataset(current_dataset)
