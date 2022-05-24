import logging

from classifiers.common import POSTCLASSIFIER_MODEL_NAME, TASK
from models.response import Response
from transformers import pipeline


logger = logging.getLogger(__name__)


HYPOTHESIS_TEMPLATE = "The user wants to {}."


class Postclassifier(object):
    def __init__(self, verbose=False):
        logger.info("Initializing postclassifier.")
        self.clf = pipeline(task="zero-shot-classification", model=POSTCLASSIFIER_MODEL_NAME)

    def __filter_responses(self, responses):
        """
            Here you can use any kind of rule-based filtration.
        """
        res = dict()

        # filter irrelevant responses (e.g. error on the server-side)
        for form, response in responses.items():
            if not response.is_irrelevant():
                res[form] = response

        return res

    def postclassify(self, query, responses) -> Response:
        """
            Filters responses based on rules, classifies responses using few-shot learning method.
            If no responses left, we should report error.
        """

        filtered_responses = self.__filter_responses(responses)

        logger.info("Forms after filtration (postclassification stage): {}".format(list(filtered_responses.keys())))

        sequence = TASK + query + " => "
        candidate_labels = list(filtered_responses.keys())

        if len(candidate_labels) > 1:
            clf_res = self.clf(sequence, candidate_labels)  # , hypothesis_template=HYPOTHESIS_TEMPLATE)
        elif len(candidate_labels) == 1:
            label = next(iter(candidate_labels))  # first and only label
            return responses[label]
        else:
            # no responses found
            return Response('Something went wrong. Please try again later.')

        # NOTE(ardulat): we can also cut by threshold if necessary
        # clf_res = cut_by_threshold(clf_res['labels'], clf_res['scores'])

        logger.info(clf_res)

        return responses[clf_res['labels'][0]]
