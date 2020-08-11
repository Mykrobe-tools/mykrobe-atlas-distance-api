from typing import List

from py2neo import Graph
from py2neo.ogm import Property, RelatedTo, RelatedFrom

from swagger_server.exceptions import NotFound
from swagger_server.models import Sample, Neighbour, NearestLeaf, Leaf
from swagger_server.ogm.base import BaseGraphObject

NEIGHBOUR_REL_TYPE = 'NEIGHBOUR'
LINEAGE_REL_TYPE = 'LINEAGE'


class LeafNode(BaseGraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()

    samples = RelatedFrom('SampleNode', LINEAGE_REL_TYPE)

    model_class = Leaf


class SampleNode(BaseGraphObject):
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', NEIGHBOUR_REL_TYPE)
    lineage = RelatedTo(LeafNode, LINEAGE_REL_TYPE)

    model_class = Sample

    @classmethod
    def create(cls, sample: Sample, graph: Graph) -> 'SampleNode':
        node = super().create(sample, graph)

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
    def update(cls, experiment_id: str, graph: Graph, neighbours: List[Neighbour] = None,
               leaf: NearestLeaf = None) -> 'SampleNode':
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
            else:
                raise NotFound

        graph.push(node)

        return node

    def detach_lineage(self, graph: Graph):
        self.lineage.clear()
        graph.push(self)

    def to_model(self) -> Sample:
        leaf_relationship = self.lineage
        neighbour_relationships = self.neighbours

        sample: Sample = super().to_model()
        sample.nearest_neighbours = []

        if len(leaf_relationship) > 0:
            leaf_node = next(iter(leaf_relationship))
            distance = self.lineage.get(leaf_node, 'distance')
            sample.nearest_leaf_node = NearestLeaf(leaf_node.leaf_id, distance)

        for neighbour_node in neighbour_relationships:
            distance = neighbour_relationships.get(neighbour_node, 'distance')
            sample.nearest_neighbours.append(Neighbour(neighbour_node.experiment_id, distance))

        return sample
