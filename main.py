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
import sys

import click
import dialogflow_v2 as dialogflow
from google.protobuf import json_format as pbjson

import aljuarismi as al

project_id = 'aljuaritmo'
session_id = al.id_session_creator()
language_code = 'en'


def detect_intent_text(project_id, session_id, text, language_code):
    """
    Detects the intent of the text and execute some instruction

    Using the same `session_id` between requests allows continuation of the conversation.

    :param project_id: ID of the project
    :param session_id: ID of the session
    :param text: The text input for analyse
    :param language_code: Code of the language
    """

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    """Conversion of Protocol Buffer to JSON"""
    response_json = pbjson.MessageToJson(response)
    data = json.loads(response_json)
    parameters = data['queryResult']['parameters']
    print(parameters)

    print('=' * 20)
    print('DEBUG: Query text: {}'.format(response.query_result.query_text))
    print('DEBUG: Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    try:
        if response.query_result.intent.display_name == 'RandomDataset':
            al.create_dataset(parameters)

        elif response.query_result.intent.display_name == 'LoadDataset':
            al.load_dataset(parameters)

        elif response.query_result.intent.display_name == 'ShowWorkspace':
            workspace = al.Workspace()
            print(list(workspace.get_all_dataset()))
        
        elif response.query_result.intent.display_name == 'GetBackend':
            al.get_library_backend(parameters['library'])

        elif response.query_result.intent.display_name == 'SetBackend':
            al.set_library_backend(parameters)

        elif response.query_result.intent.display_name == 'Exit - yes':
            al.exiting_yes(response.query_result.fulfillment_text)

        elif response.query_result.intent.display_name == 'Exit - no':
            al.exiting_no(response.query_result.fulfillment_text)

        elif not re.search("^Default|Exit", response.query_result.intent.display_name):

            if not parameters.get("Dataset"):
                parameters['Dataset'] = 'current'

            if al.check_dataset(parameters):

                if response.query_result.intent.display_name == 'ChangeName':
                    al.change_name(parameters)

                elif response.query_result.intent.display_name == 'ShowResult':
                    al.execute_plot(parameters)

                elif response.query_result.intent.display_name == 'PrintResult':
                    al.execute_print(parameters)

                elif response.query_result.intent.display_name == 'SubDatasetRow':
                    al.get_subdataset_rows(parameters)

                elif response.query_result.intent.display_name == 'SubDatasetCols':
                    al.get_subdataset_columns(parameters)

                elif response.query_result.intent.display_name == 'JoinByCols':
                    al.join_by_cols(parameters)

                elif response.query_result.intent.display_name == 'JoinByRows':
                    al.join_by_rows(parameters)

                elif response.query_result.intent.display_name == 'SplitByCols':
                    al.split_by_cols(parameters)

                elif response.query_result.intent.display_name == 'SplitByRows':
                    al.split_by_rows(parameters)

                elif response.query_result.intent.display_name == 'DoDimensionality':
                    al.do_dimensionality(parameters)

                elif response.query_result.intent.display_name == 'DoClustering':
                    al.do_clustering(parameters)

                elif response.query_result.intent.display_name == 'DoMatrix_Stomp':
                    al.do_matrix(parameters)

                elif response.query_result.intent.display_name == 'DoMatrix_Best':
                    al.do_matrix(parameters)

                elif response.query_result.intent.display_name == 'DoNormalization':
                    al.do_normalization(parameters)

                elif response.query_result.intent.display_name == 'DoFeatures':
                    al.do_features(parameters)

            else:
                if parameters["Dataset"] != 'current':
                    print("The object " + parameters["Dataset"] + " does not exist.")

                else:
                    print("There is no loaded dataset.")

                print("Please, load a dataset or use a previously stored one before using any function.")

                return

        print('DEBUG: Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

    except Exception as e:
        print('An error in the execution has been raised.')
        print(e)
        return


def main(*args, **kwargs):
    try:
        al.Workspace().init_current()
        print("Welcome, I'm Aljuarismo, what can I do for you?")
        while True:
            query = click.prompt('')
            click.echo('DEBUG: %s' % query)
            detect_intent_text(project_id, session_id, query, language_code)
    except click.exceptions.Abort:
        print('Closing the program')
        sys.exit()


if __name__ == '__main__':
    main()
