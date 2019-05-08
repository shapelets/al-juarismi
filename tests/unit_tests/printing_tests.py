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
import warnings

import dialogflow_v2 as dialogflow
from google.protobuf import json_format as pbjson

import aljuarismi as al


def response(self, txt):
    text_input = dialogflow.types.TextInput(text=txt, language_code=self.language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = self.session_client.detect_intent(session=self.session, query_input=query_input)
    response_json = pbjson.MessageToJson(response)
    return json.loads(response_json)


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)

    return do_test


class PrintingTests(unittest.TestCase):
    session_id = al.id_session_creator()

    @ignore_warnings
    def setUp(self):
        self.project_id = "aljuaritmo"
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

    def test_print(self):
        order = "Print energy"
        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'PrintResult')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PrintingTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
