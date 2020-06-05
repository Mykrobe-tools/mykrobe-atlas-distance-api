from py2neo import Subgraph, Node, Relationship, Graph

from swagger_server.models import Sample, Leaf, NearestLeaf, Neighbour


def build_graph(sample: Sample) -> Subgraph:
    sample_node = Node(Sample.__name__, experiment_id=sample.experiment_id)
    graph = sample_node

    if sample.nearest_leaf_node:
        leaf_node = Node(Leaf.__name__, leaf_id=sample.nearest_leaf_node.leaf_id)
        graph = Relationship(sample_node, 'LINEAGE', leaf_node, distance=sample.nearest_leaf_node.distance)

    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            neighbour_node = Node(Sample.__name__, experiment_id=neighbour.experiment_id)
            graph |= Relationship(sample_node, 'NEIGHBOUR', neighbour_node, distance=neighbour.distance)

    return graph


def get_sample(experiment_id: str, db: Graph) -> Sample:
    sample_node = db.nodes.match(Sample.__name__, experiment_id=experiment_id).limit(1).first()
    leaf_relationship = db.relationships.match([sample_node], 'LINEAGE')
    neighbour_relationships = db.relationships.match([sample_node], 'NEIGHBOUR')

    sample = Sample(sample_node['experiment_id'])

    if len(leaf_relationship) > 0:
        leaf_relationship = leaf_relationship.first()
        leaf_node = leaf_relationship.end_node
        sample.nearest_leaf_node = NearestLeaf(leaf_node['leaf_id'], leaf_relationship['distance'])

    if len(neighbour_relationships) > 0:
        sample.nearest_neighbours = []
        for neighbour_relationship in neighbour_relationships:
            neighbour_node = neighbour_relationship.end_node
            sample.nearest_neighbours.append(Neighbour(neighbour_node['experiment_id'], neighbour_relationship['distance']))

    return sample