from abc import ABC, abstractmethod


class AbstractGraph(ABC):
    @abstractmethod
    def add_node(self, node):
        raise NotImplementedError

    @abstractmethod
    def get_node_by_id(self, id_):
        raise NotImplementedError


class NodeNotFound(Exception):
    pass