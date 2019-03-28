#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def exiting_yes(loaded_datasets, response):
    print('Saving the workspace')
    for key in loaded_datasets.getall():
        val = loaded_datasets.get(key)
        loaded_datasets.set(key, val.to_json())
    loaded_datasets.dump()
    print('DEBUG: Fulfillment text: {}\n'.format(response))
    print('Closing program')
    exit()


def exiting_no(response):
    print('DEBUG: Fulfillment text: {}\n'.format(response))
    print('Closing program')
    exit()
