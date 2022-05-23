import re

from utils import compile_forms, retrieve_users, compile_handlers, compile_ner
from classifiers.pre import Preclassifier


class Assistant:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.forms = compile_forms()
        self.users = retrieve_users()
        # self.handlers = compile_handlers()
        self.ner = compile_ner()
        self.preclassifier = Preclassifier(verbose=verbose)

    def __retrieve_first_name(self, first_name_query):
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

    def is_user_authorized(self, phone_number):
        return phone_number in self.users

    def authorize_user(self, phone_number, first_name_query):
        if self.verbose:
            print("Authorizing user.")

        first_name = self.__retrieve_first_name(first_name_query)

        assert re.match(r"\+\d+", phone_number)
        assert re.match(r"\w+", first_name)

        self.users[phone_number] = first_name

    def match_forms(self, query):
        matched = list()

        for form, regex in self.forms.items():
            if re.match(regex, query.lower()):
                matched.append(form)

        return matched

    def handle(self, query, phone_number, call_by_name=False):
        if self.verbose:
            print("Handling query: {}".format(query))

        # match forms based on the regex
        forms = self.match_forms(query)

        # select handlers by the forms above
        # TODO(ardulat) preclassify - if connect_with_operator form exists, remove all other handlers
        forms_to_handle = self.preclassifier.preclassify(query, forms)

        # TODO(ardulat): handle forms
        # responses = self.handlers.handle(forms_to_handle)

        # TODO(ardulat): postclassify
        # final_response = self.postclassifier.postclassify(responses)

        final_response = ''
        if call_by_name:
            final_response = self.users[phone_number] + '. '
        final_response = final_response + query

        return final_response
