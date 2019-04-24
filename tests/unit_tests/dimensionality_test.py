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
    DELTA = 1e-6
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
    def test_ramer_douglas_peucker(self):
        order = 'Execute ramerDouglasPeucker on timeserie with an epsilon of 1.0'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoDimensionality')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'ramer_douglas_peucker')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')
        self.assertEqual(data['queryResult']['parameters']['number'], 1.0)

        tt = pd.DataFrame([0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0])
        self.workspace.save_dataset('timeserie', tt)
        al.do_dimensionality(data['queryResult']['parameters'])
        ramer_douglas_peucker_result = al.Workspace().get_dataset("RDP0")
        ind = ramer_douglas_peucker_result.index.to_list()
        val = ramer_douglas_peucker_result.values
        expected = [[0, 2, 3, 6, 9], [0, -0.1, 5.0, 8.1, 9.0]]
        for i in range(len(expected)):
            self.assertAlmostEqual(ind[i], expected[0][i], delta=self.DELTA)
            self.assertAlmostEqual(val[i], expected[1][i], delta=self.DELTA)

    @ignore_warnings
    def test_visvalingam(self):
        order = 'Execute visvalingam on timeserie at 5 points'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoDimensionality')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'visvalingam')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')
        self.assertEqual(data['queryResult']['parameters']['number'], 5)

        tt = pd.DataFrame([0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0])
        self.workspace.save_dataset('timeserie', tt)
        al.do_dimensionality(data['queryResult']['parameters'])
        visvalingam_result = al.Workspace().get_dataset("visvalingam0")
        ind = visvalingam_result.index.to_list()
        val = visvalingam_result.values
        expected = [[0, 2, 3, 6, 9], [0, -0.1, 5.0, 9.0, 9.0]]
        for i in range(len(expected)):
            self.assertAlmostEqual(ind[i], expected[0][i], delta=self.DELTA)
            self.assertAlmostEqual(val[i], expected[1][i], delta=self.DELTA)

    @ignore_warnings
    def test_paa(self):
        order = 'Execute paa on timeserie at 5 points'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoDimensionality')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'paa')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')
        self.assertEqual(data['queryResult']['parameters']['number'], 5)

        tt = pd.DataFrame([0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0])
        self.workspace.save_dataset('timeserie', tt)
        al.do_dimensionality(data['queryResult']['parameters'])
        paa_result = al.Workspace().get_dataset("paa0")
        val = paa_result.values
        expected = [0.05, 2.45, 6.5, 8.55, 9.0]
        for i in range(len(expected)):
            self.assertAlmostEqual(val[i], expected[i], delta=self.DELTA)

    @ignore_warnings
    def test_pip(self):
        order = 'Execute pip on timeserie at 6 points'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoDimensionality')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.85)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'pip')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')
        self.assertEqual(data['queryResult']['parameters']['number'], 6)

        tt = pd.DataFrame([0.0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0])
        self.workspace.save_dataset('timeserie', tt)
        al.do_dimensionality(data['queryResult']['parameters'])
        visvalingam_result = al.Workspace().get_dataset("pip0")
        ind = visvalingam_result.index.to_list()
        val = visvalingam_result.values
        expected = [[0, 2, 3, 6, 9], [0.0, -0.1, 5.0, 8.1, 9.0, 9.0]]
        for i in range(len(expected)):
            self.assertAlmostEqual(ind[i], expected[0][i], delta=self.DELTA)
            self.assertAlmostEqual(val[i], expected[1][i], delta=self.DELTA)

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NormalizationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
