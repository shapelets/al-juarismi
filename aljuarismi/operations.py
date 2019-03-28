#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import aljuarismi as al


def do_op(parameters, dataset, workspace):
    op = parameters.pop("Operations")
    if op == "reduction_points":
        data = al.reduce_datapoints(dataset.values, parameters)

        # workspace.set("redux", data)
        workspace = al.create_instancer("workspace")
        counters = al.create_instancer("counters")
        c = counters.get("count")
        workspace.set("val" + str(c), data.to_json())
        return data
