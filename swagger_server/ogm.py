from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.models import Sample


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

    def build_from(self, sample: Sample, graph: Graph):
        self.experiment_id = sample.experiment_id

        if sample.nearest_leaf_node:
            n = LeafNode()
            n.leaf_id = sample.nearest_leaf_node.leaf_id
            if n.exists(graph):
                self.lineage.add(n, distance=sample.nearest_leaf_node.distance)

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                n = SampleNode()
                n.experiment_id = neighbour.experiment_id
                if n.exists(graph):
                    self.neighbours.add(n, distance=neighbour.distance)
