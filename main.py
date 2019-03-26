import json
import random
import string
import sys

import click
import dialogflow_v2 as dialogflow
from google.protobuf import json_format as pbjson

import datasets as dt
import plotting as pl

random = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

project_id = 'aerial-reef-234410'
session_id = random
language_code = 'en'
datasetPaths = {}
currentDataset = None

# Container for loaded datasets
loadedDatasets = {}


def save_dictionary():
    f = open("DictionaryDataset.txt", "w+")
    for key, val in datasetPaths.items():
        f.write(key + ',' + val + '\n')
    f.close()


def load_dictionary():
    f = open("DictionaryDataset.txt", "r")
    global datasetPaths
    for line in f:
        fields = line.split(",")
        datasetPaths[fields[0]] = fields[1].rstrip()
    f.close()


def detect_intent_text(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    """Convertion of Protocol Buffer to JSON"""
    response_json = pbjson.MessageToJson(response)
    data = json.loads(response_json)
    parameters = data['queryResult']['parameters']
    print(parameters)

    print('=' * 20)
    print('DEBUG: Query text: {}'.format(response.query_result.query_text))
    print('DEBUG: Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    global currentDataset

    if response.query_result.intent.display_name == 'RandomDataset':
        pass
    elif response.query_result.intent.display_name == 'LoadDataset':
        currentDataset = dt.executeLoadDataset(parameters, loadedDatasets, datasetPaths)
    elif response.query_result.intent.display_name == 'ShowResult':
        pl.executePlot(currentDataset)
    elif response.query_result.intent.display_name == 'PrintResult':
        """Show the result of anything"""
    elif response.query_result.intent.display_name == 'Exit':
        print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

        print('Closing program')
        save_dictionary()
        exit()
    print('DEBUG: Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))


def main(*args, **kwargs):
    try:
        load_dictionary()
    except IOError:
        pass
    finally:
        pass
    try:
        while True:
            query = click.prompt('')
            click.echo('<you> %s' % query)
            detect_intent_text(project_id, session_id, query, language_code)
    except click.exceptions.Abort:
        print('Closing the program')
        sys.exit()


if __name__ == '__main__':
    main()
