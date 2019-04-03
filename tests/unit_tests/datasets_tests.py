#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import unittest


class DatasetTests(unittest.TestCase):

    def load_dataset(self):
        self.assertEqual(5, 5)

    # def setUp(self):

    # self.project_id = "aljuaritmo"
    # self.session_id = al.id_session_creator()
    # self.language_code = "en"
    # self.session_client = session_client = dialogflow.SessionsClient()
    # self. session = session_client.session_path(self.project_id, self.session_id)

    # def load_dataset(self):
    #     # order = "load titanic dataset"
    #     #
    #     # text_input = dialogflow.types.TextInput(text=order, language_code=self.language_code)
    #     # query_input = dialogflow.types.QueryInput(text=text_input)
    #     # response = self.session_client.detect_intent(session=self.session, query_input=query_input)
    #     #
    #     # response_json = pbjson.MessageToJson(response)
    #     # data = json.loads(response_json)
    #     # parameters = data['queryResult']['parameters']
    #
    #     self.assertEqual(4, 4)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DatasetTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
