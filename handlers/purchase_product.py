from models.handler import BaseHandler
from models.response import Response


class PurchaseProductHandler(BaseHandler):
    def __init__(self):
        pass

    def handle(self, form, query):
        response = Response('purchasing product')
        return response
