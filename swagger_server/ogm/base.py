from py2neo import Graph
from py2neo.ogm import GraphObject

from swagger_server.exceptions import NotFound, AlreadyExisted, MultipleFound
from swagger_server.models.base_model_ import Model


class BaseGraphObject(GraphObject):
    def exists(self, graph: Graph) -> bool:
        try:
            self.get(self.__primaryvalue__, graph)
        except NotFound:
            return False
        return True

    def to_model(self) -> Model:
        return self.model_class(self.__primaryvalue__)

    @classmethod
    def create(cls, model: Model, graph: Graph) -> 'BaseGraphObject':
        primary_value = getattr(model, cls.__primarykey__)

        node = cls()
        setattr(node, node.__primarykey__, primary_value)

        if node.exists(graph):
            raise AlreadyExisted

        graph.push(node)

        return node

    @classmethod
    def get(cls, pk, graph: Graph) -> 'BaseGraphObject':
        match = cls.match(graph, pk)
        if len(match) == 0:
            raise NotFound
        if len(match) > 1:
            raise MultipleFound
        return match.first()

    @classmethod
    def delete(cls, pk, graph: Graph):
        graph.delete(cls.get(pk, graph))
