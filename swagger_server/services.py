from typing import List

from swagger_server import registry
from swagger_server.factories import GraphFactory, ModelFactory
from swagger_server.models import Sample, Neighbour
from swagger_server.ogm import SampleNode


def create_sample(sample: Sample):
    repo = registry.get('neo4j')

    node = GraphFactory.build(sample)

    repo.create(node)


def get_sample(id_: str) -> Sample:
    repo = registry.get('neo4j')

    node = repo.get(SampleNode, id_)

    return ModelFactory.build(node)


def delete_sample(id_: str):
    repo = registry.get('neo4j')

    repo.delete(SampleNode, id_)


def get_neighbours(sample_id: str) -> List[Neighbour]:
    repo = registry.get('neo4j')

    node = repo.get(SampleNode, sample_id)

    return ModelFactory.build(node).nearest_neighbours


def update_neighbours(sample_id: str, neighbours: List[Neighbour]):
    repo = registry.get('neo4j')

    resource = Sample(sample_id, neighbours)
    node = GraphFactory.build(resource)

    repo.update(node)
