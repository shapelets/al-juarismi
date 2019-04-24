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


class NormalizationTest(unittest.TestCase):
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
    def test_znorm(self):
        order = 'Execute znorm on timeserie'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoNormalization')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'znorm')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')

        tt = pd.DataFrame([[0, 1, 2, 3], [4, 5, 6, 7]])
        self.workspace.save_dataset('timeserie', tt)
        al.do_normalization(data['queryResult']['parameters'])
        znorm_result = al.Workspace().get_dataset("znorm0").to_numpy().flatten()

        expected = [-1.341640786499870, -0.447213595499958, 0.447213595499958, 1.341640786499870]
        for i in range(len(expected)):
            self.assertAlmostEqual(znorm_result[i], expected[i], delta=self.DELTA)
            self.assertAlmostEqual(znorm_result[i + 4], expected[i], delta=self.DELTA)

    @unittest.skip
    def test_znorm_in_place(self):
        tss = Array(data=[[0, 1, 2, 3], [4, 5, 6, 7]])
        znorm_in_place(tss)
        tss = tss.to_numpy()
        self.assertAlmostEqual(tss[0][0], -1.341640786499870, delta=self.DELTA)
        self.assertAlmostEqual(tss[0][1], -0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[0][2], 0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[0][3], 1.341640786499870, delta=self.DELTA)

        self.assertAlmostEqual(tss[1][0], -1.341640786499870, delta=self.DELTA)
        self.assertAlmostEqual(tss[1][1], -0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[1][2], 0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[1][3], 1.341640786499870, delta=self.DELTA)

    @ignore_warnings
    def test_max_min_norm(self):
        order = 'Execute maximal minimal normalization on timeserie'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoNormalization')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'max_min_norm')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')

        tt = pd.DataFrame([[0, 1, 2, 3], [4, 5, 6, 7]])
        self.workspace.save_dataset('timeserie', tt)
        al.do_normalization(data['queryResult']['parameters'])

        max_min_norm_result = al.Workspace().get_dataset("max_min_norm0").to_numpy().flatten()
        expected = [0.0, 0.3333333333333, 0.66666667, 1.0]

        for i in range(len(expected)):
            self.assertAlmostEqual(max_min_norm_result[i], expected[i], delta=self.DELTA)
            self.assertAlmostEqual(max_min_norm_result[i + 4], expected[i], delta=self.DELTA)

    @ignore_warnings
    def test_max_min_norm_with_param(self):
        order = 'Execute maximal minimal normalization on timeserie with max value of 2 and min value of 1'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoNormalization')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'max_min_norm')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')
        self.assertEqual(data['queryResult']['parameters']['max'], 2)
        self.assertEqual(data['queryResult']['parameters']['min'], 1)

        tt = pd.DataFrame([[0, 1, 2, 3], [4, 5, 6, 7]])
        self.workspace.save_dataset('timeserie', tt)
        al.do_normalization(data['queryResult']['parameters'])

        max_min_norm_result = al.Workspace().get_dataset("max_min_norm0").to_numpy().flatten()
        expected = [1.0, 1.3333333333333, 1.66666667, 2.0]

        for i in range(len(expected)):
            self.assertAlmostEqual(max_min_norm_result[i], expected[i], delta=self.DELTA)
            self.assertAlmostEqual(max_min_norm_result[i + 4], expected[i], delta=self.DELTA)


    @unittest.skip
    def test_max_min_norm_in_place(self):
        tss = Array([[0, 1, 2, 3], [4, 5, 6, 7]])
        max_min_norm_in_place(tss, 2.0, 1.0)
        tss = tss.to_numpy()
        expected = np.array([[1.0, 1.3333333333333, 1.66666667, 2.0], [1.0, 1.3333333333333, 1.66666667, 2.0]])
        np.testing.assert_array_almost_equal(tss, expected, decimal=self.DECIMAL)

    @ignore_warnings
    def test_decimal_scaling_norm(self):
        order = 'Execute the decimal scaling normalization on timeserie'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoNormalization')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'decimal_scaling_norm')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')

        tt = pd.DataFrame([[0, 1, -2, 3], [40, 50, 60, -70]])
        self.workspace.save_dataset('timeserie', tt)
        al.do_normalization(data['queryResult']['parameters'])

        max_min_norm_result = al.Workspace().get_dataset("dec_sca_norm0").to_numpy().flatten()
        expected = [[0.0, 0.1, -0.2, 0.3], [0.4, 0.5, 0.6, -0.7]]

        for i in range(len(expected)):
            self.assertAlmostEqual(max_min_norm_result[i], expected[0][i], delta=self.DELTA)
            self.assertAlmostEqual(max_min_norm_result[i + 4], expected[1][i], delta=self.DELTA)

    @unittest.skip
    def test_decimal_scaling_norm_in_place(self):
        tss = Array([[0, 1, -2, 3], [40, 50, 60, -70]])
        decimal_scaling_norm_in_place(tss)
        tss = tss.to_numpy()
        expected = np.array([[0.0, 0.1, -0.2, 0.3], [0.4, 0.5, 0.6, -0.7]])
        np.testing.assert_array_almost_equal(tss, expected, decimal=self.DECIMAL)

    @ignore_warnings
    def test_mean_norm(self):
        order = 'Execute the mean norm on timeserie'

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoNormalization')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'mean_norm')
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'timeserie')

        tt = pd.DataFrame([[0, 1, 2, 3], [4, 5, 6, 7]])
        self.workspace.save_dataset('timeserie', tt)
        al.do_normalization(data['queryResult']['parameters'])

        max_min_norm_result = al.Workspace().get_dataset("mean_norm0").to_numpy().flatten()
        expected = [-0.5, -0.166666667, 0.166666667, 0.5]

        for i in range(len(expected)):
            self.assertAlmostEqual(max_min_norm_result[i], expected[i], delta=self.DELTA)
            self.assertAlmostEqual(max_min_norm_result[i + 4], expected[i], delta=self.DELTA)

    @unittest.skip
    def test_mean_norm_in_place(self):
        a = Array([[0, 1, 2, 3], [4, 5, 6, 7]])
        mean_norm_in_place(a)
        expected = np.array([[-0.5, -0.166666667, 0.166666667, 0.5], [-0.5, -0.166666667, 0.166666667, 0.5]])
        np.testing.assert_array_almost_equal(a.to_numpy(), expected, decimal=self.DECIMAL)

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NormalizationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
