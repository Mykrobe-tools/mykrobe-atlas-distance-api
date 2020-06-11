from py2neo import Graph

from swagger_server.factories import GraphFactory
from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.ogm import SampleNode


def create_sample(sample: Sample, db: Graph):
    node = GraphFactory.build(sample)
    node.create(db)


def get_sample(experiment_id: str, db: Graph) -> Sample:
    sample_node = get_graph_object(SampleNode, experiment_id, db)

    leaf_relationship = sample_node.lineage
    neighbour_relationships = sample_node.neighbours

    sample = Sample(sample_node.experiment_id)

    if len(leaf_relationship) > 0:
        leaf_node = next(iter(leaf_relationship))
        distance = sample_node.lineage.get(leaf_node, 'distance')
        sample.nearest_leaf_node = NearestLeaf(leaf_node.leaf_id, distance)

    if len(neighbour_relationships) > 0:
        sample.nearest_neighbours = []
        for neighbour_node in neighbour_relationships:
            distance = sample_node.neighbours.get(neighbour_node, 'distance')
            sample.nearest_neighbours.append(Neighbour(neighbour_node.experiment_id, distance))

    return sample


def get_graph_object(klass, primary_value, db: Graph):
    primary_key = klass.__primarykey__

    existing = klass.match(db).where(**{
        primary_key: primary_value
    }).limit(1)
    if len(existing) == 0:
        raise ObjectNotFound

    return existing.first()


def delete_sample(experiment_id: str, db: Graph):
    sample_node = get_graph_object(SampleNode, experiment_id, db)

    db.delete(sample_node)


class ObjectNotFound(Exception):
    pass


