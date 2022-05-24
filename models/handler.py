from abc import ABC, abstractmethod


class BaseHandler(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, form, query, user):
        pass
