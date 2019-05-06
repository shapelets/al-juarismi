#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import re
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

        self.project_id = "aljuaritmo"
        self.language_code = "en"
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

        self.workspace = al.Workspace()
        self.workspace.save_dataset_path('titanic', '../../datasets')
        self.workspace.init_current()

    @ignore_warnings
    def test_load_dataset(self):
        order = "load dataset titanic.csv"

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
    def test_subdataset_rows(self):
        order = "obtain a subset by rows from random0 from 10 to 60"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'SubDatasetRow')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['from'], 10)
        self.assertEqual(data['queryResult']['parameters']['to'], 60)

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        al.get_subdataset_rows(data['queryResult']['parameters'])

        dataset = al.Workspace().get_dataset('subrow0random0')

        index = dataset.index
        nrow = dataset.index.size

        self.assertEqual(index.min(), data['queryResult']['parameters']['from'])
        self.assertEqual(index.max(), data['queryResult']['parameters']['to'] - 1)
        self.assertEqual(nrow, 50)

    @ignore_warnings
    def test_subdataset_cols(self):
        order = "obtain a subset from random0 by columns at col0, col2, and col7"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'SubDatasetCols')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['cols'], ['col0', 'col2', 'col7'])

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        al.get_subdataset_columns(data['queryResult']['parameters'])

        dataset = al.Workspace().get_dataset('subcol0random0')

        ncol = dataset.columns.size
        cols = dataset.columns.to_list()
        expected = ['col0', 'col2', 'col7']

        self.assertEqual(ncol, 3)
        for n in range(3):
            self.assertEqual(cols[n], expected[n])

    @ignore_warnings
    def test_join_columns(self):
        order = "join by columns the datasets random0 and random1"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'JoinByCols')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['Dataset2'], 'random1')

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})
        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        al.join_by_cols(data['queryResult']['parameters'])

        dataset = al.Workspace().get_dataset('join0')

        ncol = dataset.columns.size
        nrow = dataset.index.size

        self.assertEqual(ncol, 20)
        self.assertEqual(nrow, 200)

    @ignore_warnings
    def test_join_rows(self):
        order = "join by rows the datasets random0 and random1"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'JoinByRows')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['Dataset2'], 'random1')

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})
        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        al.join_by_rows(data['queryResult']['parameters'])

        dataset = al.Workspace().get_dataset('join0')

        ncol = dataset.columns.size
        nrow = dataset.index.size

        self.assertEqual(ncol, 10)
        self.assertEqual(nrow, 400)

    @ignore_warnings
    def test_split_rows(self):
        order = "split random0 by 20 rows"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'SplitByRows')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['split'], 20)

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        al.split_by_rows(data['queryResult']['parameters'])

        datasets = re.findall('random0r[0-9]*', str(al.Workspace().get_all_dataset()))
        num_datasets = len(datasets)
        self.assertEqual(num_datasets, 10)
        workspace = al.Workspace()
        for num in range(num_datasets):
            dataset = workspace.get_dataset(datasets[num])
            ncol = dataset.columns.size
            nrow = dataset.index.size
            self.assertEqual(ncol, 10)
            self.assertEqual(nrow, 20)

    @ignore_warnings
    def test_split_cols(self):
        order = "split the dataset random0 by 2 columns"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'SplitByCols')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.8)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['split'], 2)

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        al.split_by_cols(data['queryResult']['parameters'])

        datasets = re.findall('random0c[0-9]*', str(al.Workspace().get_all_dataset()))
        num_datasets = len(datasets)
        self.assertEqual(num_datasets, 5)
        workspace = al.Workspace()
        for num in range(num_datasets):
            dataset = workspace.get_dataset(datasets[num])
            ncol = dataset.columns.size
            nrow = dataset.index.size
            self.assertEqual(ncol, 2)
            self.assertEqual(nrow, 200)

    @ignore_warnings
    def test_change_name(self):
        order = "rename random0 to r_a_n_d_o_m_0"

        data = response(self, order)

        self.assertEqual(data['queryResult']['intent']['displayName'], 'ChangeName')
        self.assertGreater(data['queryResult']['intentDetectionConfidence'], 0.95)
        self.assertEqual(data['queryResult']['parameters']['Dataset'], 'random0')
        self.assertEqual(data['queryResult']['parameters']['NameInto'], 'r_a_n_d_o_m_0')

        al.create_dataset({'columns': 10, 'rows': 200, 'values': [0, 1]})

        self.assertTrue(al.Workspace().get_dataset('random0') is not None)
        self.assertTrue(al.Workspace().get_dataset('r_a_n_d_o_m_0') is None)
        data1 = al.Workspace().get_dataset('random0')

        al.change_name(data['queryResult']['parameters'])

        self.assertTrue(al.Workspace().get_dataset('random0') is None)
        self.assertTrue(al.Workspace().get_dataset('r_a_n_d_o_m_0') is not None)
        data2 = al.Workspace().get_dataset('r_a_n_d_o_m_0')

        self.assertTrue(pd.DataFrame.equals(data1, data2))

    @ignore_warnings
    def tearDown(self):
        self.workspace.clean_workspace()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DatasetTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
