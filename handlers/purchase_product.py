import random
from models.handler import BaseHandler
from models.response import Response


PRODUCTS_DATABASE = {
    'book': [
        '1984 by by George Orwell',
        'A Brief History of Time by Stephen Hawking',
        'Dune (Dune Chronicles, Book 1) by Frank Herbert',
        'Fahrenheit 451 by Ray Bradbury',
        'Harry Potter and the Sorcerer\'s Stone by J.K. Rowling',
        'The Hunger Games (Book 1) by Suzanne Collins',
    ],
    'sofa': [
        'green',
        'blue',
        'white',
        'yellow',
        'brown',
    ],
}


class PurchaseProductHandler(BaseHandler):
    def __init__(self):
        print("Connecting to products database.")

    def __is_available(self, product_type, product_name):
        if product_type not in PRODUCTS_DATABASE:
            return False
        if product_name not in PRODUCTS_DATABASE[product_type]:
            return False
        return True

    def __get_product_attributes(self, query):
        product_type = ''
        product_name = ''

        if 'book' in query:
            product_type = 'book'
        elif 'sofa' in query:
            product_type = 'sofa'

        if product_type:
            product_name = random.choice(PRODUCTS_DATABASE[product_type])

        return product_type, product_name

    def handle(self, form, query):
        # TODO(ardulat): get product_type and product_name from form/frame filler
        # for now, let's just use some workaround
        product_type, product_name = self.__get_product_attributes(query)
        print("Retrieved the following product attributes: product_type - {}, product_name - {}.".format(product_type, product_name))

        if self.__is_available(product_type, product_name):
            return Response('Yes, we have it in stock. I will redirect you to our operators to place an order.')

        return Response('Sorry, we don\'t have it now. Maybe I can notify you when it\'s available?')
