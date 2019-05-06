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
import pandas as pd
from google.protobuf import json_format as pbjson
from khiva.library import set_backend, KHIVABackend

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


class DimensionalityTest(unittest.TestCase):
    DELTA = 1e-3
    DECIMAL = 6
    session_id = al.id_session_creator()

    @ignore_warnings
    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)
        self.project_id = "aljuaritmo"
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

        self.workspace = al.Workspace()
        self.workspace.init_current()

    @ignore_warnings
    def test_features(self):
        order = 'Compute features on energy'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoFeatures')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.95)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')

        tt = pd.DataFrame([[4, 4, 6, 6, 7], [4, 7, 7, 8, 8]]).transpose()
        self.workspace.save_dataset('energy', tt)
        al.do_features(data['queryResult']['parameters'])
        features_results = al.Workspace().get_dataset("energyFeatures0")

        expected = [[153.0, 242.0], [3.0, 4.0], [3.0, 4.0], [2.0, 1.0], [0.800000011920929, 0.6000000238418579],
                    [0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [-2.407405376434326, 3.2510287761688232], [1.0, 1.0],
                    [0.4000000059604645, 0.20000000298023224], [1.0, 0.0], [3.0, 4.0], [2.0, 1.0], [7.0, 8.0],
                    [0.6000000238418579, 0.800000011920929], [4.0, 4.0], [0.0, 0.0],
                    [5.40000057220459, 6.800000190734863], [6.0, 7.0], [0.6000000238418579, 0.800000011920929],
                    [0.6000000238418579, 0.6000000238418579], [-0.1656368374824524, -1.735581874847412],
                    [1.1999999284744263, 1.469693899154663], [10.0, 15.0], [27.0, 34.0],
                    [1.4399999380111694, 2.1600000858306885], [1.0, 1.0]]
        for i in range(len(expected)):
            self.assertAlmostEqual(features_results[0][i], expected[i][0], delta=self.DELTA)
            self.assertAlmostEqual(features_results[1][i], expected[i][1], delta=self.DELTA)

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NormalizationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
