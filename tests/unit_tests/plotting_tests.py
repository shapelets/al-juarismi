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


class PlottingTests(unittest.TestCase):
    session_id = al.id_session_creator()

    @ignore_warnings
    def setUp(self):
        self.project_id = "aljuaritmo"
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

    def test_plot(self):
        order = "Plot energy"
        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'ShowResult')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')

    def test_plot_any_columns(self):
        order = "Plot titanic for Fare and Age"
        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'ShowResult')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'titanic')
        self.assertEqual(data['queryResult']['parameters']['columns'], ['Fare', 'Age'])

    def test_plot_from_to(self):
        order = "Plot titanic from 10 to 30"
        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'ShowResult')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'titanic')
        self.assertEqual(data['queryResult']['parameters']['from'], 10)
        self.assertEqual(data['queryResult']['parameters']['to'], 30)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PlottingTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
