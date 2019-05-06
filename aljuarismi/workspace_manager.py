#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pandas as pd
import pickledb as pdb


class Workspace:

    path = ""

    def __init__(self):

        if Workspace.path == "":
            Workspace.path = os.getcwd()

        self.path_resources = Workspace.path + "/resources"

        if not os.path.exists(self.path_resources):
            os.mkdir(self.path_resources)

        datasets_path = self.path_resources + '/datasets.db'
        counters_path = self.path_resources + '/counters.db'
        dataset_locator_path = self.path_resources + '/dataset_locator.db'

        self.__datasets = pdb.load(datasets_path, auto_dump=True)
        self.__counters = pdb.load(counters_path, auto_dump=True)
        self.__dataset_locator = pdb.load(dataset_locator_path, auto_dump=True)

    def init_current(self):
        """
        Initialize the current dataset
        """
        self.__datasets.set('current', None)

    def clean_workspace(self):
        """
        Delete all databases.
        """
        self.remove_all()
        self.__dataset_locator.deldb()

    def save_dataset(self, name, dataset, path=''):
        """
        Stores a dataset with the given name.
        :param name: The name of the dataset.
        :param dataset: The object dataset.
        :param path: The path where is located the dataset. (By default is a empty string).
        """
        if path:
            self.__dataset_locator.set(name, path)
        try:
            if isinstance(dataset, pd.DataFrame):
                self.__datasets.set(name, dataset.to_json())
            else:
                self.__datasets.set(name, dataset)
        except AttributeError:
            print("La estoy cagando.")

    def get_dataset(self, name):
        """
        Returns a dataset.
        :param name: The name of the dataset.
        :return: The object dataset.
        """

        data = self.__datasets.get(name)
        if data:
            try:
                if isinstance(data, list):
                    return pd.read_json(data[0]).sort_index()
                else:
                    return pd.read_json(data).sort_index()
            except ValueError:
                return data
        else:
            return None

    def get_value(self, name):
        """
        Return the dataset without any transformation or the tuple.
        :param name: The name of the key (dataset name or variable name).
        :return: The dataset/tuple.
        """
        return self.__datasets.get(name)

    def remove_dataset(self, name):
        """
        Removes a dataset.
        :param name: The name of the dataset.
        """
        self.__datasets.rem(name)

    def get_all_dataset(self):
        """
        Returns all datasets stored in dataset.
        """
        return self.__datasets.getall()

    def remove_all(self):
        """
        Remove all datasets stored in the workspace.
        """
        self.__datasets.deldb()
        self.__counters.deldb()
        self.__dataset_name.deldb()

    def get_dataset_path(self, name):
        """
        Obtains the path where is located a dataset.
        :param name: The name of the dataset.
        :return: The path of a dataset.
        """
        path = self.__dataset_locator.get(name)
        if path:
            return path
        else:
            return None

    def get_all_dataset_paths(self):
        """
        Obtains all the names of the datasets which have a stored path.
        """
        return self.__dataset_locator.getall()

    def get_counter(self, name):
        """
        Obtains the number of a counter and increment that counter.
        :param name: The name of the counter.
        :return: The number of the counter.
        """
        num = self.__counters.get(name)
        if not num:
            num = 0
        self.__counters.set(name, num + 1)
        return num

    def get_last_number_counter(self, name):
        """
        Obtains the last number generated of a counter.
        :param name: The name of the counter.
        :return: The last number generated of the counter.
        """
        num = self.__counters.get(name) - 1
        if not num or num < 0:
            num = 0
        return num

    def save_dataset_path(self, dataset_name, dataset_path):
        """
        Saves only the path where the dataset is located.
        :param dataset_name: The name of the dataset.
        :param dataset_path: The path where is located the dataset.
        """
        self.__dataset_locator.set(dataset_name, dataset_path)

    def has_any_dataset(self):
        """
        Sees if the database of datasets has any dataset saved, except of the current.
        :return: Boolean.
        """
        return self.__datasets.totalkeys() > 1

