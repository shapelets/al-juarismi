#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import aljuarismi


def execute_print(current_dataset, parameters):
    """
    Execute the print function.
    :param current_dataset: The current dataset.
    :param parameters: The parameter for the print (Dataset name, ...).
    :return:
    """
    data_name = parameters["Dataset"]
    if data_name == '' or data_name == 'current_dataset':
        print(current_dataset)
    else:
        dataset = aljuarismi.Workspace().get_dataset(data_name)
        print(dataset)
