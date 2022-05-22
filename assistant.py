import re

from collections import defaultdict
from transformers import pipeline


def compile_grammars():
    # TODO(ardulat): should be verbose only
    print('Compiling grammars.')
    pass


def retrieve_users():
    # TODO(ardulat): should be verbose only
    print('Retrieving users from database.')
    # NOTE(ardulat): here can be your SQL query to retrieve all signed users from a database
    # or instead you can retrieve user info on each query (better not to store all users in runtime)

    users = dict()
    with open('users.tsv') as f:
        for line in f:
            phone_number, first_name = line.strip().split('\t')

            assert re.match(r"\+\d+", phone_number)
            assert re.match(r"\w+", first_name)

            users[phone_number] = first_name

    return users


def compile_handlers():
    # TODO(ardulat): should be verbose only
    print('Compiling handlers.')
    pass


def compile_ner():
    # TODO(ardulat): should be verbose only
    print('Compiling NER.')

    # NOTE(ardulat): you can also use 'en_core_web_sm' NER provided by spacy, but it's not that accurate.
    ner = pipeline('ner', model='elastic/distilbert-base-cased-finetuned-conll03-english')
    return ner


class Assistant:
    def __init__(self, verbose=False):
        # self.grammars = compile_grammars()
        self.users = retrieve_users()
        # self.handlers = compile_handlers()
        self.verbose = verbose
        self.ner = compile_ner()

    def is_user_authorized(self, phone_number):
        return phone_number in self.users

    def authorize_user(self, phone_number, first_name_query):
        if self.verbose:
            print("Authorizing user.")

        first_name = self.retrieve_first_name(first_name_query)

        assert re.match(r"\+\d+", phone_number)
        assert re.match(r"\w+", first_name)

        self.users[phone_number] = first_name

    def handle(self, query, phone_number, call_by_name=False):
        if self.verbose:
            print("Handling query: {}".format(query))
        response = 'Okay'
        if call_by_name:
            response = response + ', ' + self.users[phone_number]
        response = response + '. ' + query

        return response

    def retrieve_first_name(self, first_name_query):
        # Response to 'How can I call you?' might not be always the name only.
        # Thus, we need to retrieve the name from the query using taggers.
        res = self.ner(first_name_query)
        if self.verbose:
            print(res)
        first_name = ''

        for entity in res:
            if entity['entity'] == 'B-PER':
                first_name = entity['word']

        return first_name

