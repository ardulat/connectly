import random

from models.handler import BaseHandler
from models.response import Response


RESPONSES = [
    'Sure, you are always welcome!',
    'Sure, welcome!',
    'Welcome :)',
    'No problem.'
]

class ThankHandler(BaseHandler):
    def __init__(self):
        pass

    def handle(self, form, query, user):
        response = random.choice(RESPONSES)
        return Response(response)