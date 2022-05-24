from models.handler import BaseHandler
from models.response import Response


PURCHASE_DATABASE = {
    '+77472447424': [
        'book',
        'sofa',
    ],
    '+88888888888': [
        'toy',
    ],
}

class ReturnProductHandler(BaseHandler):
    def __init__(self):
        print("Connecting to purchase database.")

    def __get_product_type(self, query, user):
        if user not in PURCHASE_DATABASE:
            return ''
        for product in PURCHASE_DATABASE[user]:
            if product in query:
                return product
        return ''

    def __has_purchased_items(self, user):
        return user in PURCHASE_DATABASE

    def __has_purchased(self, user, product):
        return product in PURCHASE_DATABASE[user]

    def handle(self, form, query, user):
        # TODO(ardulat): get product type from form/frame
        # for now, here is a workaround
        product_type = self.__get_product_type(query, user)

        if not self.__has_purchased_items(user):
            return Response("Oppsie! You haven't purchased anything from us.")
        elif not self.__has_purchased(user, product_type):
            return Response("Opps! You haven't purchased this item from us.")

        return Response('We are sorry to hear that. I will initiate a return process. ' + \
            'Our operators will connect with you to share details on how to return {}.'.format(product_type))
