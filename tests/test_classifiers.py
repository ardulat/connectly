import pytest

from assistant import Assistant
from models.response import Response


FIRST_CANDIDATE_RESPONSES = {
    'purchase_product': Response('purchase_product response'),
    'ask_for_recommendation': Response('ask_for_recommendation response'),
}
SECOND_CANDIDATE_RESPONSES = {
    'purchase_product': Response('purchase_product response'),
    'thank': Response('thank response')
}


class TestClassifiers(object):
    @pytest.fixture(scope='class')
    def assistant(self):
        return Assistant(verbose=True)

    @pytest.mark.parametrize('query, forms', [
        ('i would like to purchase a sofa', ['purchase_product']),
        ('i would like to purchase a sofa, thank you', ['purchase_product', 'thank']),
        ('connect me with operator', ['connect_with_operator']),
        ('something out of domain so that we can talk', ['connect_with_operator']),
    ])
    def test_preclassifier(self, assistant, query, forms):
        assert assistant
        assert assistant.preclassifier

        matched_forms = assistant.match_forms(query)

        assert assistant.preclassifier.preclassify(query, matched_forms) == forms

    @pytest.mark.parametrize('query, candidate_responses, final_response_text', [
        ('I would like to purchase a sofa', FIRST_CANDIDATE_RESPONSES, 'purchase_product response'),
        ('Thank you so much', SECOND_CANDIDATE_RESPONSES, 'thank response'),
    ])
    def test_postclassifier(self, assistant, query, candidate_responses, final_response_text):
        assert assistant
        assert assistant.postclassifier

        response = assistant.postclassifier.postclassify(query, candidate_responses)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == final_response_text
