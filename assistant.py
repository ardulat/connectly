import re

from classifiers.pre import Preclassifier
from handlers.handlers import Handlers
from utils import compile_forms, retrieve_users, compile_ner


class Assistant:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.forms = compile_forms()
        self.users = retrieve_users()
        self.ner = compile_ner()
        self.handlers = Handlers(verbose=verbose)
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

        # select forms to handle based on preclassifier
        forms_to_handle = self.preclassifier.preclassify(query, forms)

        # TODO(ardulat): handle forms
        responses = self.handlers.handle(forms_to_handle, query)

        # TODO(ardulat): postclassify
        # final_response = self.postclassifier.postclassify(responses)

        final_response = responses[0].text_response
        if call_by_name:
            prefix = self.users[phone_number] + ', '
            final_response = final_response[0].lower() + final_response[1:]
            final_response = prefix + final_response

        return final_response
