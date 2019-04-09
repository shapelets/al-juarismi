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

import click
import pyttsx3 as tts

import aljuarismi.workspace_manager as wm


def id_session_creator():
    """
    Creates the random string which will be used in the session_id.
    :return: The random string.
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def query_input():
    query = ''
    while query == '':
        query = click.prompt('')
    return query


def check_dataset(parameters):
    """
    Check if the current dataset or, it is passed the name, a dataset exists or not.
    :param parameters: The parameters for this function (name of the Dataset)
    :return: If the dataset exists.
    """
    workspace = wm.Workspace()
    dataset_name = parameters['Dataset']
    check = workspace.get_dataset(dataset_name)

    return check is not None


def isnumber(value):
    """
    Checks if it is a number the input.
    :param value: The number in string.
    :return: A boolean.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def voice(txt):
    """
    Reproduces the message passed.
    :param txt: The text which will be read.
    :return:
    """
    v = tts.init()
    v.say(txt)
    v.runAndWait()
