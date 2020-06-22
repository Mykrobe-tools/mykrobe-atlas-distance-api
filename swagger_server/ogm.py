from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.exceptions import NotFound


class BaseGraphObject(GraphObject):
    @classmethod
    def get(cls, primary_value, graph: Graph) -> 'BaseGraphObject':
        match = cls.match(graph, primary_value).limit(1)
        if len(match) == 0:
            raise NotFound
        return match.first()

    def exists(self, graph: Graph) -> bool:
        try:
            self.get(self.__primaryvalue__, graph)
        except NotFound:
            return False
        else:
            return True


class LeafNode(BaseGraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(BaseGraphObject):
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
