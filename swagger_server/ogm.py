from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.exceptions import Existed
from swagger_server.models import Sample


class BaseGraphObject(GraphObject):
    def exists(self, graph: Graph) -> bool:
        return len(self.match(graph, self.__primaryvalue__)) > 0


class LeafNode(GraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(BaseGraphObject):
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')

    @classmethod
    def create_from(cls, sample: Sample, graph: Graph):
        node = cls()
        node.experiment_id = sample.experiment_id

        if node.exists(graph):
            raise Existed

        graph.create(node)

        if sample.nearest_leaf_node and len(LeafNode.match(graph, sample.nearest_leaf_node.leaf_id)) > 0:
            n = LeafNode()
            n.leaf_id = sample.nearest_leaf_node.leaf_id
            node.lineage.add(n, distance=sample.nearest_leaf_node.distance)

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                if len(SampleNode.match(graph, neighbour.experiment_id)) > 0:
                    n = SampleNode()
                    n.experiment_id = neighbour.experiment_id
                    node.neighbours.add(n, distance=neighbour.distance)

        graph.push(node)

        return node
