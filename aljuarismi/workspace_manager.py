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

    def __init__(self):
        self.path = os.getcwd()
        self.path_resources = self.path + "/resources"

        if not os.path.exists(self.path_resources):
            os.mkdir(self.path_resources)

        datasets_path = self.path_resources + '/datasets.db'
        counters_path = self.path_resources + '/counters.db'
        dataset_locator_path = self.path_resources + '/dataset_locator.db'

        self.__datasets = pdb.load(datasets_path, True)
        self.__counters = pdb.load(counters_path, True)
        self.__dataset_locator = pdb.load(dataset_locator_path, True)

    def clean_workspace(self):
        """
        Delete all databases.
        :return:
        """
        self.remove_all()
        self.__dataset_locator.deldb()

    def save_dataset(self, name, dataset, path=''):
        """
        Stores a dataset with the given name.
        :param name:
        :param dataset:
        :return:
        """
        if path:
            self.__dataset_locator.set(name, path)
        self.__datasets.set(name, dataset.to_json())

    def get_dataset(self, name):
        """
        Returns the dataset corresponding to name.
        :param name:
        :return:
        """
        return pd.read_json(self.__datasets.get(name))

    def remove_dataset(self, name):
        """
        Removes the dataset with name.
        :param name:
        :return:
        """
        self.__datasets.rem(name)

    def get_all_dataset(self):
        """
        Returns all datasets stored in workspace.
        :return:
        """
        return self.__datasets.getall()

    def remove_all(self):
        """
        Remove all datasets stored in the workspace
        :return:
        """
        self.__datasets.deldb()
        self.__counters.deldb()

    def get_dataset_count(self, name):
        """

        :return:
        """
        return self.__counters.get(name)

    def get_dataset_path(self, name):
        """

        :param name:
        :return:
        """
        return self.__dataset_locator.get(name)

    def get_all_dataset_paths(self):
        """

        :return:
        """
        return self.__dataset_locator.getall()

    def get_counter(self, name):
        """

        :param name:
        :return:
        """
        num = self.__counters.get(name)
        self.__counters.set(name, num + 1)
        return num

    def save_dataset_path(self, dataset_name, dataset_path):
        """

        :param dataset_name:
        :param dataset_path:
        :return:
        """
        self.__dataset_locator.set(dataset_name, dataset_path)
