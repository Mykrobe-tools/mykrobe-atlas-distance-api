from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.ogm import SampleNode


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
