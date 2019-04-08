#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import string

import pyttsx3 as tts

import aljuarismi.workspace_manager as wm


def id_session_creator():
    """
    Creates the random string which will be used in the session_id.
    :return: The random string.
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def check_dataset(parameters):
    """
    Check if the current dataset or, it is passed the name, a dataset exists or not.
    :param parameters: The parameters for this function (name of the Dataset)
    :return: If the dataset exists.
    """
    workspace = wm.Workspace()
    dataset_name = parameters['Dataset']
    check = workspace.get_dataset('current') is not None or (dataset_name in list(workspace.get_all_dataset()))
    if not check:
        if workspace.has_any_dataset():
            print("Please, load a database before using any function or use a saved one in the workspace")
        else:
            print("Please, load a database before using any workspace")
    return check


def voice(txt):
    """
    Reproduces the message passed.
    :param txt: The text which will be read.
    :return:
    """
    v = tts.init()
    v.say(txt)
    v.runAndWait()
