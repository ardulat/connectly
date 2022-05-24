import pytest

from handlers.ask_for_recommendation import AskForRecommendationHandler
from handlers.connect_with_operator import ConnectWithOperatorHandler
from handlers.purchase_product import PurchaseProductHandler
from handlers.return_product import ReturnProductHandler
from handlers.thank import ThankHandler


RECOMMENDATIONS_BOOK = [
    '1984 by by George Orwell',
    'A Brief History of Time by Stephen Hawking',
    'Dune (Dune Chronicles, Book 1) by Frank Herbert',
    'Fahrenheit 451 by Ray Bradbury',
    'Harry Potter and the Sorcerer\'s Stone by J.K. Rowling',
    'The Hunger Games (Book 1) by Suzanne Collins',
]
RECOMMENDATIONS_OTHER = [
    'MacBook',
    'Windows 8',
    'Windows Vista',
    'Windows 10',
    'Kali Linux',
    'Ubuntu',
]

class TestHandlers(object):

    @pytest.fixture(scope='class')
    def user(self):
        return '+77472447424'

    @pytest.mark.parametrize('query', [
        'connect me with operator',
        'can i talk to human?',
    ])
    def test_connect_with_operator_handler(self, query, user):
        form = 'connect_with_operator'
        expected_response = 'Redirecting you to operator.'
        handler = ConnectWithOperatorHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == expected_response

    @pytest.mark.parametrize('query', [
        'thank you so much',
        'great, thanks',
    ])
    def test_thank_handler(self, query, user):
        form = 'thank'
        expected_responses = [
            'Sure, you are always welcome!',
            'Sure, welcome!',
            'Welcome :)',
            'No problem.'
        ]
        handler = ThankHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response in expected_responses

    @pytest.mark.parametrize('query, expected_response', [
        ('i would like to purchase a sofa', 'Yes, we have it in stock. I will redirect you to our operators to place an order.'),
        ('i would like to purchase a book', 'Yes, we have it in stock. I will redirect you to our operators to place an order.'),
        ('i would like to purchase a burger', 'Unfortunately, we don\'t have it now.'),
    ])
    def test_purchase_product_handler(self, query, expected_response, user):
        form = 'purchase_product'
        handler = PurchaseProductHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == expected_response

    @pytest.mark.parametrize('query, expected_entity', [
        ('i would like to return a sofa', 'sofa'),
        ('i would like to return a book', 'book'),
    ])
    def test_return_product_handler_purchased(self, query, expected_entity, user):
        form = 'return_product'
        expected_response = 'We are sorry to hear that. I will initiate a return process. ' + \
            'Our operators will connect with you to share details on how to return ' + expected_entity + '.'
        handler = ReturnProductHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == expected_response

    def test_return_product_handler_not_purchased_item(self, user):
        form = 'return_product'
        query = 'i would like to return a burger'
        handler = ReturnProductHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == "Opps! You haven't purchased this item from us."

    def test_return_product_handler_not_purchased_user(self):
        form = 'return_product'
        query = 'i would like to return a book'
        user = '+77777777777'
        handler = ReturnProductHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()
        assert response.text_response == "Oppsie! You haven't purchased anything from us."

    @pytest.mark.parametrize('query, expected_recommendations', [
        ('can you recommend me a book?', RECOMMENDATIONS_BOOK),
        ('can you recommend me an operating system?', RECOMMENDATIONS_OTHER),
    ])
    def test_ask_for_recommendation_handler(self, query, expected_recommendations, user):
        form = 'ask_for_recommendation'
        expected_prefix = 'Here are few recommendations: '
        handler = AskForRecommendationHandler()

        response = handler.handle(form, query, user)

        assert response
        assert not response.is_irrelevant()

        text_response = response.text_response
        assert text_response.startswith(expected_prefix)

        recommendations_string = text_response.split(': ')[-1]
        recommendations_list = recommendations_string[:-1].split(', ')
        assert len(recommendations_list) == 3
        for r in recommendations_list:
            assert r in expected_recommendations

