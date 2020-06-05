from abc import ABC, abstractmethod


class AbstractGraph(ABC):
    @abstractmethod
    def add_node(self, **attributes):
        raise NotImplementedError

    @abstractmethod
    def get_node(self, **attributes):
        raise NotImplementedError
