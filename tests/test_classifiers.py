import pytest

from ..assistant import Assistant
from ..classifiers.pre import Preclassifier


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

