#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import aljuarismi as al


def exiting_yes(response):
    """
    Exit the program saving the workspace.
    :param response: The response from Dialogflow.
    """
    print('Saving the workspace')
    al.voice('Saving the workspace')
    print('Saved workspace')
    al.voice('Saved workspace')
    print('DEBUG: Fulfillment text: {}'.format(response))
    al.voice(response)
    print('Closing program')
    al.voice('Closing program')
    exit()


def exiting_no(response):
    """
    Exit the program deleting the workspace.
    :param response: The response from Dialogflow.
    """
    print('Deleting workspace')
    al.voice('Deleting workspace')
    al.Workspace().clean_workspace()
    print('Deleted workspace')
    al.voice('Deleted workspace')
    print('DEBUG: Fulfillment text: {}'.format(response))
    al.voice(response)
    print('Closing program')
    al.voice('Closing program')
    exit()

