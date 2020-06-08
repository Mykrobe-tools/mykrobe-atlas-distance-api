from py2neo import Graph
from py2neo.ogm import GraphObject, RelatedTo, Property

from swagger_server.models import Sample, Leaf, NearestLeaf, Neighbour


class LeafNode(GraphObject):
    __primarylabel__ = Leaf.__name__
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(GraphObject):
    __primarylabel__ = Sample.__name__
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')


def create_sample(sample: Sample, db: Graph):
    existing_node = SampleNode.match(db).where(experiment_id=sample.experiment_id)
    if len(existing_node) > 0:
        raise SampleExisted

    sample_node = SampleNode()
    sample_node.experiment_id = sample.experiment_id

    if sample.nearest_leaf_node:
        leaf_node = LeafNode()
        leaf_node.leaf_id = sample.nearest_leaf_node.leaf_id
        sample_node.lineage.add(leaf_node, distance=sample.nearest_leaf_node.distance)

    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            if neighbour.experiment_id != sample.experiment_id:
                neighbour_node = SampleNode()
                neighbour_node.experiment_id = neighbour.experiment_id
                sample_node.neighbours.add(neighbour_node, distance=neighbour.distance)

    db.create(sample_node)


def get_sample(experiment_id: str, db: Graph) -> Sample:
    sample_node = SampleNode.match(db).where(experiment_id=experiment_id).limit(1)
    if len(sample_node) == 0:
        raise SampleNotFound
    sample_node = sample_node.first()

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


def delete_sample(experiment_id: str, db: Graph):
    sample_node = SampleNode.match(db).where(experiment_id=experiment_id).limit(1)
    if len(sample_node) == 0:
        raise SampleNotFound
    sample_node = sample_node.first()

    db.delete(sample_node)


class SampleNotFound(Exception):
    pass


class SampleExisted(Exception):
    pass
