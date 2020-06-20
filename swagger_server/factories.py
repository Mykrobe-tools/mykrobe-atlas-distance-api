from py2neo import Graph

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.ogm import SampleNode, LeafNode


class SampleFactory:
    @staticmethod
    def build(recipe: SampleNode) -> Sample:
        leaf_relationship = recipe.lineage
        neighbour_relationships = recipe.neighbours

        sample = Sample(recipe.experiment_id)
        sample.nearest_neighbours = []

        if len(leaf_relationship) > 0:
            leaf_node = next(iter(leaf_relationship))
            distance = recipe.lineage.get(leaf_node, 'distance')
            sample.nearest_leaf_node = NearestLeaf(leaf_node.leaf_id, distance)

        if len(neighbour_relationships) > 0:
            for neighbour_node in neighbour_relationships:
                distance = recipe.neighbours.get(neighbour_node, 'distance')
                sample.nearest_neighbours.append(Neighbour(neighbour_node.experiment_id, distance))

        return sample


class SampleNodeFactory:
    @staticmethod
    def build(recipe: Sample, graph: Graph) -> SampleNode:
        node = SampleNode()
        node.experiment_id = recipe.experiment_id

        if recipe.nearest_leaf_node:
            n = LeafNode()
            n.leaf_id = recipe.nearest_leaf_node.leaf_id
            if n.exists(graph):
                node.lineage.add(n, distance=recipe.nearest_leaf_node.distance)

        if recipe.nearest_neighbours:
            for neighbour in recipe.nearest_neighbours:
                n = SampleNode()
                n.experiment_id = neighbour.experiment_id
                if n.exists(graph):
                    node.neighbours.add(n, distance=neighbour.distance)

        return node
