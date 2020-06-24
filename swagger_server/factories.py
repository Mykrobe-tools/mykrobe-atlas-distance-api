from abc import ABC, abstractmethod
from typing import Any, List

from py2neo.ogm import RelatedObjects

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.ogm import SampleNode


class Factory(ABC):
    @staticmethod
    @abstractmethod
    def build(recipe) -> Any:
        raise NotImplementedError


class SampleFactory(Factory):
    @staticmethod
    def build(recipe: SampleNode) -> Sample:
        leaf_relationship = recipe.lineage
        neighbour_relationships = recipe.neighbours

        sample = Sample(recipe.experiment_id)

        if len(leaf_relationship) > 0:
            leaf_node = next(iter(leaf_relationship))
            distance = recipe.lineage.get(leaf_node, 'distance')
            sample.nearest_leaf_node = NearestLeaf(leaf_node.leaf_id, distance)

        sample.nearest_neighbours = NeighboursFactory.build(neighbour_relationships)

        return sample


class NeighboursFactory(Factory):
    @staticmethod
    def build(recipe: RelatedObjects) -> List[Neighbour]:
        neighbours = []

        for neighbour_node in recipe:
            distance = recipe.get(neighbour_node, 'distance')
            neighbours.append(Neighbour(neighbour_node.experiment_id, distance))

        return neighbours
