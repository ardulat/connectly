import logging
import pytest

from assistant import Assistant
from models.response import Response


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')


FIRST_CANDIDATE_RESPONSES = {
    'ask_for_recommendation': Response('ask_for_recommendation response'),
    'purchase_product': Response('purchase_product response'),
}
SECOND_CANDIDATE_RESPONSES = {
    'purchase_product': Response('purchase_product response'),
    'thank': Response('thank response'),
}
THIRD_CANDIDATE_RESPONSES = {
    'ask_for_recommendation': Response('ask_for_recommendation response'),
    'purchase_product': Response('purchase_product response'),
    'thank': Response('thank response'),
}


class TestClassifiers(object):
    @pytest.fixture(scope='class')
    def assistant(self):
        return Assistant()

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
        ('I would like to purchase a sofa, thanks in advance', SECOND_CANDIDATE_RESPONSES, 'purchase_product response'),
        ('I would like to buy a recommended book', FIRST_CANDIDATE_RESPONSES, 'purchase_product response'),
        ('Thank you so much', {'thank': Response('thank response')}, 'thank response'),
        ('can i purchase a recommended book? thanks in advance', THIRD_CANDIDATE_RESPONSES, 'purchase_product response'),
    ])
    def test_postclassifier(self, assistant, query, candidate_responses, final_response_text):
        assert assistant
        assert assistant.postclassifier

        response = assistant.postclassifier.postclassify(query, candidate_responses)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == final_response_text
