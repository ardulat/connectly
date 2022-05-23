from models.handler import BaseHandler
from models.response import Response


class ThankHandler(BaseHandler):
    def __init__(self):
        pass

    def handle(self, form, query):
        return Response('Sure, you are always welcome!')