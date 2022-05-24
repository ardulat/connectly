import pytest

from assistant import Assistant
from utils import compile_forms


class TestForms(object):

    @pytest.fixture(scope='class')
    def assistant(self):
        return Assistant(verbose=True)

    @pytest.mark.parametrize('query, forms', [
        ('can i talk to human', ['connect_with_operator']),
        ('thank you', ['thank']),
        ('i would like to purchase a sofa', ['purchase_product']),
        ('i would like to purchase a sofa, thank you', ['purchase_product', 'thank']),
        ('can you please recommend me a sofa for my cousin?', ['ask_for_recommendation']),
        ('can i return the purchased sofa?', ['return_product']),
    ])
    def test_positive(self, assistant, query, forms):
        assert assistant
        assert assistant.forms
        assert assistant.match_forms(query) == forms
