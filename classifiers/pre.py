from classifiers.common import PRECLASSIFIER_MODEL_NAME, TASK
from transformers import pipeline


CONNECT_WITH_OPERATOR_FORM = 'connect_with_operator'


class Preclassifier(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        if verbose:
            print("Initializing preclassifier.")
        self.clf = pipeline(task="zero-shot-classification", model=PRECLASSIFIER_MODEL_NAME)

    def __filter_forms(self, forms):
        """
            Here you can use any kind of rule-based filtration.
        """
        res = forms

        # prioritize forms
        if CONNECT_WITH_OPERATOR_FORM in forms or not forms:  # if no matched forms present
            res = [CONNECT_WITH_OPERATOR_FORM]

        return res

    def preclassify(self, query, forms):
        """
            Filters forms based on rules, classifies forms using few-shot learning method.
            If only one form is left after filtration, returns it as a list.
        """

        filtered_forms = self.__filter_forms(forms)

        if self.verbose:
            print("Forms after filtration (preclassification stage):")
            print(filtered_forms)

        sequence = TASK + "\n" + query + " => "
        candidate_labels = filtered_forms

        if len(candidate_labels) > 1:
            clf_res = self.clf(sequence, candidate_labels)
        else:
            # no need to run inference for one single label
            return candidate_labels

        # NOTE(ardulat): we can also cut by threshold if necessary
        # clf_res = cut_by_threshold(clf_res['labels'], clf_res['scores'])

        if self.verbose:
            print(clf_res)

        return clf_res['labels']
