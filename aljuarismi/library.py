#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import khiva as kv


def get_backend():
    """
    Execute the function get_backend of Khiva and print the result.
    """
    backend = kv.get_backend()
    backend_name = re.search('(_[^_]*)$', backend.name).group()[1:]
    print('The current backend is ' + backend_name)


def get_backends():
    """
     Execute the function get_backends of Khiva and print which backends has the computer.
    """
    backends = kv.get_backends()
    cuda = kv.KHIVABackend.KHIVA_BACKEND_CUDA.value & backends
    cpu = kv.KHIVABackend.KHIVA_BACKEND_CPU.value & backends
    opencl = kv.KHIVABackend.KHIVA_BACKEND_OPENCL.value & backends
    print('Your computer has the following backends:')
    if cpu:
        print('\tCPU')
    if cuda:
        print('\tCUDA')
    if opencl:
        print('\tOPENCL')


def set_backend(backend):
    """
     Execute the function set_backend of Khiva.
    :param backend: The backend to set.
    """
    if backend == 'CPU':
        kv.set_backend(kv.KHIVABackend.KHIVA_BACKEND_CPU)
    elif backend == 'CUDA':
        kv.set_backend(kv.KHIVABackend.KHIVA_BACKEND_CUDA)
    elif backend == 'OPENCL':
        kv.set_backend(kv.KHIVABackend.KHIVA_BACKEND_OPENCL)
