#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from aljuarismi import utilities as ut
from aljuarismi import workspace_manager as wpm


def exiting_yes(response):
    print('Saving the workspace')
    ut.voice('Saving the workspace')
    print('Saved workspace')
    ut.voice('Saved workspace')
    print('DEBUG: Fulfillment text: {}'.format(response))
    ut.voice(response)
    print('Closing program')
    ut.voice('Closing program')
    exit()


def exiting_no(response):
    print('Deleting workspace')
    ut.voice('Deleting workspace')
    restart()
    print('Deleted workspace')
    ut.voice('Deleted workspace')
    print('DEBUG: Fulfillment text: {}'.format(response))
    ut.voice(response)
    print('Closing program')
    ut.voice('Closing program')
    exit()


def restart():
    path = os.path.realpath(os.path.dirname(__file__))
    os.remove(path + "/../resources/workspace.db")
    counters = wpm.create_instancer("counters")
    for key in counters.getall():
        counters.set(key, 0)
