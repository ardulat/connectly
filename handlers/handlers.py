from handlers.connect_with_operator import ConnectWithOperatorHandler


HANDLERS_MAP = {
    'connect_with_operator': ConnectWithOperatorHandler(),
}


class Handlers(object):
    def __init__(self, verbose=False):
        self.handlers = HANDLERS_MAP

    def handle(self, forms_to_handle, query):
        """
            Handle forms based on the forms to handlers map.
            Returns list of responses - List[Response].
        """

        responses = list()

        for form in forms_to_handle:
            assert form in self.handlers, "No handler found for form {} form!".format(form)

            response = self.handlers[form].handle(form, query)
            responses.append(response)

        return responses
