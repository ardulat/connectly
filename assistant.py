import logging
import re

from classifiers.pre import Preclassifier
from classifiers.post import Postclassifier
from handlers.handlers import Handlers
from utils import compile_forms, retrieve_users, compile_ner


logger = logging.getLogger(__name__)


class Assistant:
    def __init__(self):
        logger.info("Waking up assistant.")
        self.forms = compile_forms()
        self.users = retrieve_users()
        self.ner = compile_ner()
        self.handlers = Handlers()
        self.preclassifier = Preclassifier()
        self.postclassifier = Postclassifier()

    def __retrieve_first_name(self, first_name_query):
        # Response to 'How can I call you?' might not be always the name only.
        # Thus, we need to retrieve the name from the query using taggers.
        res = self.ner(first_name_query)
        logger.info(res)
        first_name = ''

        for entity in res:
            if entity['entity'] == 'B-PER':
                first_name = entity['word']

        assert first_name, "Could not retrieve the name from the query!"

        return first_name

    def is_user_authorized(self, phone_number):
        return phone_number in self.users

    def authorize_user(self, phone_number, first_name_query):
        logger.info("Authorizing user.")

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
        logger.info("Handling query: {}".format(query))

        # match forms based on the regex
        forms = self.match_forms(query)

        # select forms to handle based on preclassifier
        forms_to_handle = self.preclassifier.preclassify(query, forms)

        # walk through form handlers and collect responses
        responses = self.handlers.handle(forms_to_handle, query, phone_number)

        # select form to respond based on postclassifier
        final_response = self.postclassifier.postclassify(query, responses).text_response

        if call_by_name:
            prefix = self.users[phone_number] + ', '
            final_response = final_response[0].lower() + final_response[1:]
            final_response = prefix + final_response

        return final_response
