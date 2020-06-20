from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo


class BaseGraphObject(GraphObject):
    def exists(self, graph: Graph) -> bool:
        return len(self.match(graph, self.__primaryvalue__)) > 0


class LeafNode(BaseGraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(BaseGraphObject):
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
