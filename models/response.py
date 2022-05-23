class Response(object):
    def __init__(self, text_response=''):
        self.text_response = text_response
        self.irrelevant = False
        self.should_callback = ''

    def is_irrelevant(self):
        return self.irrelevant

    def set_irrelevant(self):
        self.irrelevant = True

    def set_should_callback(self, form):
        self.should_callback = form
