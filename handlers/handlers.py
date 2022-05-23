from handlers.ask_for_recommendation import AskForRecommendationHandler
from handlers.connect_with_operator import ConnectWithOperatorHandler
from handlers.purchase_product import PurchaseProductHandler
from handlers.thank import ThankHandler


HANDLERS_MAP = {
    'ask_for_recommendation': AskForRecommendationHandler(),
    'connect_with_operator': ConnectWithOperatorHandler(),
    'purchase_product': PurchaseProductHandler(),
    'thank': ThankHandler(),
}


class Handlers(object):
    def __init__(self, verbose=False):
        self.handlers = HANDLERS_MAP

    def handle(self, forms_to_handle, query):
        """
            Handle forms based on the forms to handlers map.
            Returns dictionary of form to responses - Dict[Response].
        """

        responses = dict()

        for form in forms_to_handle:
            assert form in self.handlers, "No handler found for form {} form!".format(form)

            response = self.handlers[form].handle(form, query)
            responses[form] = response

        return responses
