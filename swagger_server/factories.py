from functools import singledispatchmethod

from py2neo.ogm import GraphObject

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.models.base_model_ import Model
from swagger_server.ogm.mappers import LeafNode, SampleNode


class ModelFactory:
    @singledispatchmethod
    @staticmethod
    def build(recipe: GraphObject) -> Model:
        raise NotImplementedError

    @build.register(SampleNode)
    @staticmethod
    def _(recipe: SampleNode) -> Sample:
        leaf_relationship = recipe.lineage
        neighbour_relationships = recipe.neighbours

        sample = Sample(recipe.experiment_id)

        if len(leaf_relationship) > 0:
            leaf_node = next(iter(leaf_relationship))
            distance = recipe.lineage.get(leaf_node, 'distance')
            sample.nearest_leaf_node = NearestLeaf(leaf_node.leaf_id, distance)

        if len(neighbour_relationships) > 0:
            sample.nearest_neighbours = []
            for neighbour_node in neighbour_relationships:
                distance = recipe.neighbours.get(neighbour_node, 'distance')
                sample.nearest_neighbours.append(Neighbour(neighbour_node.experiment_id, distance))

        return sample


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
