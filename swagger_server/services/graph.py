from py2neo import Subgraph, Node, Relationship, Graph

from swagger_server.models import Sample, Leaf, NearestLeaf


def build_graph(sample: Sample) -> Subgraph:
    sample_node = Node(Sample.__name__, experiment_id=sample.experiment_id)
    graph = sample_node

    if sample.nearest_leaf_node:
        leaf_node = Node(Leaf.__name__, leaf_id=sample.nearest_leaf_node.leaf_id)
        graph = Relationship(sample_node, 'LINEAGE', leaf_node, distance=sample.nearest_leaf_node.distance)

    return graph


def get_sample(experiment_id: str, db: Graph) -> Sample:
    sample_node = db.nodes.match(Sample.__name__, experiment_id=experiment_id).limit(1).first()
    nearest_leaf_node = db.relationships.match([sample_node], 'LINEAGE')

    sample = Sample(sample_node['experiment_id'])

    if len(nearest_leaf_node) > 0:
        nearest_leaf_node = nearest_leaf_node.first()
        sample.nearest_leaf_node = NearestLeaf(nearest_leaf_node.end_node['leaf_id'], nearest_leaf_node['distance'])

    return sample