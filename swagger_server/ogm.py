from typing import List

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.exceptions import AlreadyExisted, NotFound
from swagger_server.models import Sample, NearestLeaf, Neighbour


class BaseGraphObject(GraphObject):
    def exists(self, graph: Graph) -> bool:
        try:
            self.get(self.__primaryvalue__, graph)
        except NotFound:
            return False
        return True

    @classmethod
    def create(cls, pk, graph: Graph) -> 'BaseGraphObject':
        node = cls()
        setattr(node, node.__primarykey__, pk)

        if node.exists(graph):
            raise AlreadyExisted

        graph.push(node)

        return node

    @classmethod
    def get(cls, experiment_id: str, graph: Graph) -> 'BaseGraphObject':
        match = cls.match(graph, experiment_id).limit(1)
        if len(match) == 0:
            raise NotFound
        return match.first()

    @classmethod
    def delete(cls, experiment_id: str, graph: Graph):
        graph.delete(cls.get(experiment_id, graph))


class LeafNode(BaseGraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(BaseGraphObject):
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')

    @classmethod
    def create(cls, sample: Sample, graph: Graph) -> 'SampleNode':
        node = super().create(sample.experiment_id, graph)

        if sample.nearest_leaf_node:
            n = LeafNode()
            n.leaf_id = sample.nearest_leaf_node.leaf_id
            if n.exists(graph):
                node.lineage.add(n, distance=sample.nearest_leaf_node.distance)

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                n = cls()
                n.experiment_id = neighbour.experiment_id
                if n.exists(graph):
                    node.neighbours.add(n, distance=neighbour.distance)

        graph.push(node)

        return node

    @classmethod
    def update(cls, experiment_id: str, graph: Graph, neighbours: List[Neighbour] = None, leaf: NearestLeaf = None) -> 'SampleNode':
        node = cls.get(experiment_id, graph)

        if neighbours is not None:
            node.neighbours.clear()

            for neighbour in neighbours:
                n = SampleNode()
                n.experiment_id = neighbour.experiment_id
                if n.exists(graph):
                    node.neighbours.add(n, distance=neighbour.distance)

        if leaf is not None:
            node.lineage.clear()

            n = LeafNode()
            n.leaf_id = leaf.leaf_id
            if n.exists(graph):
                node.lineage.add(n, distance=leaf.distance)

        graph.push(node)

        return node

    def to_model(self) -> Sample:
        leaf_relationship = self.lineage
        neighbour_relationships = self.neighbours

        sample = Sample(self.experiment_id, nearest_neighbours=[])

        if len(leaf_relationship) > 0:
            leaf_node = next(iter(leaf_relationship))
            distance = self.lineage.get(leaf_node, 'distance')
            sample.nearest_leaf_node = NearestLeaf(leaf_node.leaf_id, distance)

        for neighbour_node in neighbour_relationships:
            distance = neighbour_relationships.get(neighbour_node, 'distance')
            sample.nearest_neighbours.append(Neighbour(neighbour_node.experiment_id, distance))

        return sample
