import logging

from models.handler import BaseHandler
from models.response import Response


logger = logging.getLogger(__name__)


class ConnectWithOperatorHandler(BaseHandler):
    def __init__(self):
        logger.info("Connecting with operators.")

    def handle(self, form, query, user):
        # Here you can check if free operators available.
        # If not, ask the user to wait and keep searching for free operators.

        return Response('Redirecting you to operator.')
