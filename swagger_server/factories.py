from functools import singledispatchmethod

from py2neo.ogm import GraphObject

from swagger_server.models import Sample
from swagger_server.models.base_model_ import Model
from swagger_server.ogm import LeafNode, SampleNode


class GraphFactory:
    @singledispatchmethod
    @staticmethod
    def build(recipe: Model) -> GraphObject:
        raise NotImplementedError

    @build.register(Sample)
    @staticmethod
    def _(recipe: Sample) -> SampleNode:
        node = SampleNode()
        node.experiment_id = recipe.experiment_id

        if recipe.nearest_leaf_node:
            leaf_node = LeafNode()
            leaf_node.leaf_id = recipe.nearest_leaf_node.leaf_id
            node.lineage.add(leaf_node, distance=recipe.nearest_leaf_node.distance)

        if recipe.nearest_neighbours:
            for neighbour in recipe.nearest_neighbours:
                if neighbour.experiment_id != recipe.experiment_id:
                    neighbour_node = SampleNode()
                    neighbour_node.experiment_id = neighbour.experiment_id
                    node.neighbours.add(neighbour_node, distance=neighbour.distance)

        return node
