import logging
import random

from models.handler import BaseHandler
from models.response import Response


logger = logging.getLogger(__name__)


RESPONSES = [
    'Sure, you are always welcome!',
    'Sure, welcome!',
    'Welcome :)',
    'No problem.'
]


class ThankHandler(BaseHandler):
    def __init__(self):
        logger.info("Collecting \"Thank you\" phrases.")

    def handle(self, form, query, user):
        response = random.choice(RESPONSES)
        return Response(response)
