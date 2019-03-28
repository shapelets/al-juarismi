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


def id_session_creator():
    """
    Creates the random string which will be use in the session_id
    :return: The random string
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

