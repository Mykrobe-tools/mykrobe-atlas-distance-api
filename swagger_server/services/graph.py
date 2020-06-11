from py2neo import Graph

from swagger_server.factories import GraphFactory, ModelFactory
from swagger_server.models import Sample
from swagger_server.ogm import SampleNode


def create_sample(sample: Sample, db: Graph):
    node = GraphFactory.build(sample)
    node.create(db)


def get_sample(experiment_id: str, db: Graph):
    sample_node = SampleNode.get(experiment_id, db)
    return ModelFactory.build(sample_node)


def delete_sample(experiment_id: str, db: Graph):
    sample_node = SampleNode.get(experiment_id, db)

    db.delete(sample_node)


