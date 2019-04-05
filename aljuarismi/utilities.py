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


def check_current_dataset(dataset):
    """
    Check if the current dataset exists or not.
    :param dataset: The current dataset.
    :return: If the dataset exists
    """
    workspace = wm.Workspace()
    if dataset is None:
        if workspace.has_any_dataset():
            print("Please, load a database before using any function or use a saved one in the database")
        else:
            print("Please, load a database before using any function")
        return False
    return True


def voice(txt):
    """
    Does the voice of the assistant.
    :param txt: The text which will be read.
    :return:
    """
    v = tts.init()
    v.say(txt)
    v.runAndWait()
