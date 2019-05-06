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


class MatrixTest(unittest.TestCase):
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
    def test_stomp_self_join(self):
        order = "Execute stomp self join on energy with subsequence length of 3"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoMatrix_Stomp')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'stomp_self_join')
        self.assertEqual(data['queryResult']['parameters']['m'], 3)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')

        tt1 = pd.DataFrame([10, 10, 11, 11, 10, 11, 10, 10, 11, 11, 10, 11, 10, 10])
        self.workspace.save_dataset('energy', tt1)

        expected_index = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]

        al.do_matrix(data['queryResult']['parameters'])
        stomp_self_join_result = al.Workspace().get_dataset('stomp0')
        for i in range(6):
            self.assertAlmostEqual(stomp_self_join_result['profile'].to_numpy()[i], 0.0, delta=1e-2)
            self.assertEqual(stomp_self_join_result['index'].to_numpy()[i], expected_index[i])

    @ignore_warnings
    def test_stomp(self):
        order = "Execute stomp on energy and consumption with a subsequence length of 3"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoMatrix_Stomp')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'stomp')
        self.assertEqual(data['queryResult']['parameters']['m'], 3)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'energy')
        self.assertEqual(data['queryResult']['parameters']['Dataset2'], 'consumption')

        tt1 = pd.DataFrame([10, 11, 10, 11])
        tt2 = pd.DataFrame([10, 11, 10, 11, 10, 11, 10, 11])
        self.workspace.save_dataset('energy', tt1)
        self.workspace.save_dataset('consumption', tt2)

        expected_index = [0, 1, 0, 1, 0, 1]

        al.do_matrix(data['queryResult']['parameters'])
        stomp_result = al.Workspace().get_dataset('stomp0')
        for i in range(6):
            self.assertAlmostEqual(stomp_result['profile'].to_numpy()[i], 0, delta=1e-2)
            self.assertAlmostEqual(stomp_result['index'].to_numpy()[i], expected_index[i])

    @ignore_warnings
    def test_find_best_n_motifs(self):
        order = "Execute stomp on energy and consumption with a subsequence length of 3"

        data = response(self, order)

        tt1 = pd.DataFrame([10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9])
        tt2 = pd.DataFrame([10, 11, 10, 9])
        self.workspace.save_dataset('energy', tt1)
        self.workspace.save_dataset('consumption', tt2)

        al.do_matrix(data['queryResult']['parameters'])

        order = "Find best 1 motif from stomp0"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoMatrix_Best')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'find_best_n_motifs')
        self.assertEqual(data['queryResult']['parameters']['n'], 1)

        al.do_matrix(data['queryResult']['parameters'])

        find_best_n_motifs_result = al.Workspace().get_dataset('motifs0')

        for i in range(3):
            self.assertEqual(find_best_n_motifs_result['col0'][i], 10)

    @ignore_warnings
    def test_find_best_n_discords(self):
        order = "Execute stomp on energy and consumption with a subsequence length of 3"

        data = response(self, order)

        tt1 = pd.DataFrame([11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11])
        tt2 = pd.DataFrame([9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 9])
        self.workspace.save_dataset('energy', tt1)
        self.workspace.save_dataset('consumption', tt2)

        al.do_matrix(data['queryResult']['parameters'])

        order = "Find best 2 discords from stomp0"

        data = response(self, order)
        self.assertEqual(data['queryResult']['intent']['displayName'], 'DoMatrix_Best')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['operation'], 'find_best_n_discords')
        self.assertEqual(data['queryResult']['parameters']['n'], 2)

        al.do_matrix(data['queryResult']['parameters'])

        find_best_n_discord_result = al.Workspace().get_dataset('discords0')

        expected_result = [11, 10, 11]

        for i in range(1):
            col = find_best_n_discord_result['col' + str(i)].tolist()
            for j in range(2):
                self.assertEqual(col[j], expected_result[j])

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatrixTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
