#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import os
import unittest
import warnings

import dialogflow_v2 as dialogflow
import pandas as pd
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


class DatasetTests(unittest.TestCase):
    session_id = al.id_session_creator()

    @ignore_warnings
    def setUp(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/franco.gonzalez/Desktop/Credentials/" \
                                                       "Aljuaritmo-3ac32e58ff41.json"
        self.project_id = "aljuaritmo"
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

        self.workspace = al.Workspace()
        self.workspace.save_dataset_path('titanic', '../../datasets')
        self.workspace.init_current()

    @ignore_warnings
    def test_load_dataset(self):
        order = "load dataset titanic"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'LoadDataset')
        self.assertEqual(data['queryResult']['intentDetectionConfidence'], 1.0)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'titanic')

        al.load_dataset(data['queryResult']['parameters'])
        self.workspace = al.Workspace()
        dataset = self.workspace.get_dataset('current')
        titanic = pd.read_csv("../../datasets/titanic.csv")
        self.assertEqual(dataset.to_json(), titanic.to_json())

    @ignore_warnings
    def test_create_random(self):
        order = "create random dataset for 5 row and 10 columns between -12.1 and 80"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'RandomDataset')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        al.create_dataset(data['queryResult']['parameters'])
        self.workspace = al.Workspace()
        random = self.workspace.get_dataset('current')
        self.assertEqual(random.shape, (int(data['queryResult']['parameters']['rows']),
                                        int(data['queryResult']['parameters']['columns'])),
                         '(n_row, n_column) do not match')
        self.assertGreaterEqual(random.values.min(), float(data['queryResult']['parameters']['values'][0]))
        self.assertLessEqual(random.values.max(), float(data['queryResult']['parameters']['values'][1]))

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DatasetTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
