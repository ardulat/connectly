import random

from models.handler import BaseHandler
from models.response import Response


PRODUCTS = {
    'book': [
        '1984 by by George Orwell',
        'A Brief History of Time by Stephen Hawking',
        'Dune (Dune Chronicles, Book 1) by Frank Herbert',
        'Fahrenheit 451 by Ray Bradbury',
        'Harry Potter and the Sorcerer\'s Stone by J.K. Rowling',
        'The Hunger Games (Book 1) by Suzanne Collins',
    ],
    'other': [
        'MacBook',
        'Windows 8',
        'Windows Vista',
        'Windows 10',
        'Kali Linux',
        'Ubuntu',
    ]
}


class AskForRecommendationHandler(BaseHandler):
    def __init__(self):
        # initialize recommendation system
        print("Initializing recommendation system.")

    def handle(self, form, query, user):
        text_response = 'Here are few recommendations: '

        # here we can check if some certain slots in form are present
        products = []
        if 'book' in query: # but instead I will use query for now (because we don't have slots yet)
            products = PRODUCTS['book']
        else:
            products = PRODUCTS['other']

        # choose randomly 3 of them
        # ofc, this is not how recommendation systems should work :)
        recommendations = random.sample(products, k=3)
        for r in recommendations:
            text_response = text_response + r + ', '
        text_response = text_response[:-2] + '.'

        response = Response(text_response)

        return response
