#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import aljuarismi as al


def execute_print(dataset, parameters):
    """
    Execute the print function.
    :param dataset: The current dataset.
    :param parameters: The parameter for the print (Dataset name, ...).
    :return:
    """
    workspace = al.Workspace()
    data_name = parameters["Dataset"]
    if data_name:
        dataset = workspace.get_dataset(data_name)
        if dataset is None:
            return
    print(dataset)
