#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import unittest

import dialogflow_v2 as dialogflow
from google.protobuf import json_format as pbjson
from khiva.library import *

import aljuarismi as al


def response(self, txt):
    text_input = dialogflow.types.TextInput(text=txt, language_code=self.language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = self.session_client.detect_intent(session=self.session, query_input=query_input)
    response_json = pbjson.MessageToJson(response)
    return json.loads(response_json)


class LibraryTest(unittest.TestCase):
    session_id = al.id_session_creator()

    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)
        self.project_id = "aljuaritmo"
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

    def test_get_backend(self):
        order = 'give me the current backend'
        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'GetBackend')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['library'], 'backend')

    def test_get_backends(self):
        order = 'get all backends'
        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'GetBackend')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['library'], 'backends')

    def test_set_backend(self):
        backends = get_backends()
        cuda = backends & KHIVABackend.KHIVA_BACKEND_CUDA.value
        opencl = backends & KHIVABackend.KHIVA_BACKEND_OPENCL.value
        cpu = backends & KHIVABackend.KHIVA_BACKEND_CPU.value
        b = get_backend()
        if cuda:
            order = 'set CUDA backend'
            data = response(self, order)
            self.assertEqual(data['queryResult']['intent']['displayName'], 'SetBackend')
            self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
            self.assertEqual(data['queryResult']['parameters']['library'], 'backend')
            self.assertEqual(data['queryResult']['parameters']['backend'].upper(), 'CUDA')

            al.set_library_backend(data['queryResult']['parameters'])
            self.assertEqual(get_backend(), KHIVABackend.KHIVA_BACKEND_CUDA)
            set_backend(b)

        if opencl:
            order = 'set OpenCL backend'
            data = response(self, order)
            self.assertEqual(data['queryResult']['intent']['displayName'], 'SetBackend')
            self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
            self.assertEqual(data['queryResult']['parameters']['library'], 'backend')
            self.assertEqual(data['queryResult']['parameters']['backend'], 'OpenCL')

            al.set_library_backend(data['queryResult']['parameters'])
            self.assertEqual(get_backend(), KHIVABackend.KHIVA_BACKEND_OPENCL)
            set_backend(b)

        if cpu:
            order = 'set CPU backend'
            data = response(self, order)
            self.assertEqual(data['queryResult']['intent']['displayName'], 'SetBackend')
            self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
            self.assertEqual(data['queryResult']['parameters']['library'], 'backend')
            self.assertEqual(data['queryResult']['parameters']['backend'], 'CPU')

            al.set_library_backend(data['queryResult']['parameters'])
            self.assertEqual(get_backend(), KHIVABackend.KHIVA_BACKEND_CPU)
            set_backend(b)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NormalizationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
