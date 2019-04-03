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


class DatasetTests(unittest.TestCase):

    def setUp(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/franco.gonzalez/Desktop/Credentials/" \
                                                       "Aljuaritmo-3ac32e58ff41.json"
        self.project_id = "aljuaritmo"
        self.session_id = al.id_session_creator()
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

        self.workspace = al.Workspace()
        self.workspace.save_dataset_path('titanic', '../../datasets')

    def test_load_dataset(self):
        order = "load dataset titanic"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'LoadDataset')
        self.assertEqual(data['queryResult']['intentDetectionConfidence'], 1.0)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'titanic')

        dataset = al.execute_load_dataset(data['queryResult']['parameters'])
        titanic = pd.read_csv("../../datasets/titanic.csv")
        self.assertEqual(dataset.to_json(), titanic.to_json())

    def test_create_random_not_param(self):
        order = "Create random dataset"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'RandomDataset')
        self.assertEqual(data['queryResult']['intentDetectionConfidence'], 1.0)
        random = al.create_dataset(data['queryResult']['parameters'])
        self.assertEqual(random.size, 50)
        self.assertIn(random.values.all(), range(0, 50))

    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DatasetTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
