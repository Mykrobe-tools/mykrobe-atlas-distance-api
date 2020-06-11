from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.exceptions import Exists, NotFound
from swagger_server.models import Leaf, Sample


class GraphModel(GraphObject):
    def create(self, graph: Graph):
        if self.exists(graph):
            raise Exists

        graph.create(self)

    @classmethod
    def get(cls, pk, graph: Graph):
        matched = cls.match(graph, pk).limit(1)

        if len(matched) == 0:
            raise NotFound

        return matched.first()

    def exists(self, graph: Graph):
        existing = self.match(graph).where(**{
            self.__primarykey__: self.__primaryvalue__
        })

        return len(existing) > 0


class LeafNode(GraphObject):
    __primarylabel__ = Leaf.__name__
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(GraphModel):
    __primarylabel__ = Sample.__name__
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
