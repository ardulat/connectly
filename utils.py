import json
import logging
import re

from transformers import pipeline


logger = logging.getLogger(__name__)


def compile_forms():
    """
        Compiles forms provided in forms/ directory.
        The result is form to regex dictionary.
    """
    logger.info('Compiling forms.')
    forms = dict()

    with open('forms/config.json', 'r') as f:
        config = json.load(f)

        for cfg in config:
            form = cfg['form']

            regex = []
            with open('forms/' + cfg['path'], 'r') as ft:
                for line in ft:
                    regex.append(line.strip().lower())
            regex_string = '|'.join(regex)

            forms[form] = re.compile(regex_string)

    return forms


def retrieve_users():
    logger.info('Retrieving users from database.')

    # NOTE(ardulat): here can be your SQL query to retrieve all signed users from a database
    # or instead you can retrieve user info on each query (better not to store all users in runtime)

    users = dict()
    with open('data/users.tsv', 'r') as f:
        for line in f:
            phone_number, first_name = line.strip().split('\t')

            assert re.match(r"\+\d+", phone_number)
            assert re.match(r"\w+", first_name)

            users[phone_number] = first_name

    return users


def compile_ner():
    logger.info('Initializing Named-Entity Recognition.')

    # NOTE(ardulat): you can also use 'en_core_web_sm' NER provided by spacy, but it's not that accurate.
    ner = pipeline('ner', model='elastic/distilbert-base-cased-finetuned-conll03-english')
    return ner
