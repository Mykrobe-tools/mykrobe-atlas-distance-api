from typing import Any, Union

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.models import Sample, Leaf
from swagger_server.models.base_model_ import Model

NEIGHBOUR_REL_TYPE = 'NEIGHBOUR'
LINEAGE_REL_TYPE = 'LINEAGE'


class BaseGraphObject(GraphObject):
    @classmethod
    def primary_key_exists(cls, primary_value: Any, graph: Graph) -> bool:
        kwargs = {
            cls.__primarykey__: primary_value
        }
        return len(cls.match(graph).where(**kwargs)) > 0

    @staticmethod
    def from_model(model: Model) -> Union['BaseGraphObject']:
        raise NotImplementedError


class LeafNode(BaseGraphObject):
    __primarykey__ = 'name'

    name = Property()

    @staticmethod
    def from_model(leaf: Leaf) -> Union['LeafNode']:
        node = LeafNode()
        node.name = leaf.leaf_id

        return node


class SampleNode(BaseGraphObject):
    __primarykey__ = 'name'

    name = Property()

    neighbours = RelatedTo('SampleNode', NEIGHBOUR_REL_TYPE)
    lineage = RelatedTo(LeafNode, LINEAGE_REL_TYPE)

    @staticmethod
    def from_model(sample: Sample) -> Union['SampleNode']:
        node = SampleNode()
        node.name = sample.experiment_id

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                neighbour_node = SampleNode()
                neighbour_node.name = neighbour.experiment_id
                node.neighbours.add(neighbour_node, distance=neighbour.distance)

        if sample.nearest_leaf_node:
            leaf_node = LeafNode()
            leaf_node.name = sample.nearest_leaf_node.leaf_id
            node.lineage.add(leaf_node, distance=sample.nearest_leaf_node.distance)

        return node