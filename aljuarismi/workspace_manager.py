#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pickledb as pdb


def create_instancer(type):
    """
    Factory for the instancer of each database
    :param type: Type of the database (workspace, dataset_locator, counters)
    :return: The loaded database
    """
    if type == "workspace":
        return pdb.load('resources/workspace.db', True)
    if type == "dataset_locator":
        return pdb.load('resources/dataset_locator.db', True)
    if type == "counters":
        return pdb.load('resources/counters.db', True)
