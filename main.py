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

    Using the same `session_id` between requests allows continuation
    of the conversation.

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

    if response.query_result.intent.display_name == 'RandomDataset':
        al.create_dataset(parameters)

    elif response.query_result.intent.display_name == 'LoadDataset':
        al.load_dataset(parameters)

    elif response.query_result.intent.display_name == 'ShowWorkspace':
        workspace = al.Workspace()
        print(list(workspace.get_all_dataset()))

    elif response.query_result.intent.display_name == 'Exit - yes':
        al.exiting_yes(response.query_result.fulfillment_text)

    elif response.query_result.intent.display_name == 'Exit - no':
        al.exiting_no(response.query_result.fulfillment_text)

    elif not re.search("^Default|Exit", response.query_result.intent.display_name):
        if al.check_dataset(parameters):

            if response.query_result.intent.display_name == 'ShowResult':
                al.execute_plot(parameters)

            elif response.query_result.intent.display_name == 'PrintResult':
                al.execute_print(parameters)

            elif response.query_result.intent.display_name == 'DoOperations':
                al.do_op(parameters)

            elif response.query_result.intent.display_name == 'DoClustering':
                al.do_clustering(parameters)

    print('DEBUG: Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
    if response.query_result.fulfillment_text:
        al.voice(response.query_result.fulfillment_text)


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
