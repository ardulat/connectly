from models.handler import BaseHandler
from models.response import Response


class AskForRecommendationHandler(BaseHandler):
    def __init__(self):
        #initialize recommendation system
        print("Initializing recommendation system.")

    def handle(self, form, query):
        response = Response('here are few recommendations: blahblah')

        return response
