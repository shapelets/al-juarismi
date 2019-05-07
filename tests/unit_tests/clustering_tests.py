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


class ClusteringTests(unittest.TestCase):
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
    def test_kmeans(self):
        order = "Do the kmeans of 3 clusters"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoClustering')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'kmeans')
        self.assertEqual(data['queryResult']['parameters']['number'], 3)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], '')
        tts = pd.DataFrame([[0.0, 1.0, 2.0, 3.0],
                            [6.0, 7.0, 8.0, 9.0],
                            [2.0, -2.0, 4.0, -4.0],
                            [8.0, 5.0, 3.0, 1.0],
                            [15.0, 10.0, 5.0, 0.0],
                            [7.0, -7.0, 1.0, -1.0]])

        expected_c = pd.DataFrame([[0.0, 0.1667, 0.3333, 0.5],
                                   [1.5, -1.5, 0.8333, -0.8333],
                                   [4.8333, 3.6667, 2.6667, 1.6667]])

        (centroid, labels) = al.kmean(tts, data['queryResult']['parameters'])

        for i in range(len(expected_c)):
            self.assertAlmostEqual(centroid[0][i], expected_c[0][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[1][i], expected_c[1][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[2][i], expected_c[2][i], delta=self.DELTA)

    @ignore_warnings
    def test_kmeans_dataset(self):
        order = "Do the kmeans of 3 clusters for energy"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoClustering')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'kmeans')
        self.assertEqual(data['queryResult']['parameters']['number'], 3)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')

        tts = pd.DataFrame([[0.0, 1.0, 2.0, 3.0],
                            [6.0, 7.0, 8.0, 9.0],
                            [2.0, -2.0, 4.0, -4.0],
                            [8.0, 5.0, 3.0, 1.0],
                            [15.0, 10.0, 5.0, 0.0],
                            [7.0, -7.0, 1.0, -1.0]])

        self.workspace.save_dataset('energy', tts)

        expected_c = pd.DataFrame([[0.0, 0.1667, 0.3333, 0.5],
                                   [1.5, -1.5, 0.8333, -0.8333],
                                   [4.8333, 3.6667, 2.6667, 1.6667]])

        al.do_clustering(data['queryResult']['parameters'])

        (centroid, labels) = (al.Workspace().get_dataset('centroids0'), al.Workspace().get_dataset('labels0'))

        for i in range(len(expected_c)):
            self.assertAlmostEqual(centroid[0][i], expected_c[0][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[1][i], expected_c[1][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[2][i], expected_c[2][i], delta=self.DELTA)

    @ignore_warnings
    def test_kshape(self):
        order = "Do the kshape of 3 clusters"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoClustering')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.9)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'kshape')
        self.assertEqual(data['queryResult']['parameters']['number'], 3)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], '')
        tts = pd.DataFrame([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                            [0.0, 10.0, 4.0, 5.0, 7.0, -3.0, 0.0],
                            [-1.0, 15.0, -12.0, 8.0, 9.0, 4.0, 5.0],
                            [2.0, 8.0, 7.0, -6.0, -1.0, 2.0, 9.0],
                            [-5.0, -5.0, -6.0, 7.0, 9.0, 9.0, 0.0]])

        expected_c = pd.DataFrame([[-0.5234, 0.1560, -0.3627, -1.2764, -0.7781, 0.9135, 1.8711],
                                   [-0.7825, 1.5990, 0.1701, 0.4082, 0.8845, -1.4969, -0.7825],
                                   [-0.6278, 1.3812, -2.0090, 0.5022, 0.6278, 0.0000, 0.1256]])

        (centroid, labels) = al.kshape(tts, data['queryResult']['parameters'])

        for i in range(len(expected_c)):
            self.assertAlmostEqual(centroid[0][i], expected_c[0][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[1][i], expected_c[1][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[2][i], expected_c[2][i], delta=self.DELTA)

    @ignore_warnings
    def test_shape_dataset(self):
        order = "Do the kshape of 3 clusters for energy"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoClustering')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'kshape')
        self.assertEqual(data['queryResult']['parameters']['number'], 3)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')

        tts = pd.DataFrame([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                            [0.0, 10.0, 4.0, 5.0, 7.0, -3.0, 0.0],
                            [-1.0, 15.0, -12.0, 8.0, 9.0, 4.0, 5.0],
                            [2.0, 8.0, 7.0, -6.0, -1.0, 2.0, 9.0],
                            [-5.0, -5.0, -6.0, 7.0, 9.0, 9.0, 0.0]])

        self.workspace.save_dataset('energy', tts)

        expected_c = pd.DataFrame([[-0.5234, 0.1560, -0.3627, -1.2764, -0.7781, 0.9135, 1.8711],
                                   [-0.7825, 1.5990, 0.1701, 0.4082, 0.8845, -1.4969, -0.7825],
                                   [-0.6278, 1.3812, -2.0090, 0.5022, 0.6278, 0.0000, 0.1256]])

        al.do_clustering(data['queryResult']['parameters'])

        (centroid, labels) = (al.Workspace().get_dataset('centroids0'), al.Workspace().get_dataset('labels0'))

        for i in range(len(expected_c)):
            self.assertAlmostEqual(centroid[0][i], expected_c[0][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[1][i], expected_c[1][i], delta=self.DELTA)
            self.assertAlmostEqual(centroid[2][i], expected_c[2][i], delta=self.DELTA)

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClusteringTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
