from hypothesis import given, assume
from hypothesis.strategies import from_type, lists

from swagger_server.adapters.object_mappers.neo4j import SampleNode, NEIGHBOUR_REL_TYPE
from swagger_server.models import Sample, Neighbour


@given(sample=from_type(Sample))
def test_creating_new_sample(db, client, sample):
    try:
        response = client.open('/api/v1/samples', method='POST', json=sample)

        assert response.status_code == 201
        assert len(db.graph.nodes.match(SampleNode.__primarylabel__, name=sample.experiment_id)) == 1
    finally:
        db.truncate()


def test_creating_duplicated_sample_returns_error(sample_repo, db, client):
    experiment_id = 'some id'
    sample = Sample(experiment_id)
    sample_repo.add(sample)

    response = client.open('/api/v1/samples', method='POST', json=sample)

    assert response.status_code == 409
    assert len(db.graph.nodes.match(SampleNode.__primarylabel__, name=sample.experiment_id)) == 1


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour), unique_by=lambda n: n.experiment_id))
def test_creating_sample_with_non_duplicated_and_new_neighbours(db, client, sample, neighbours):
    assume(sample.experiment_id not in [n.experiment_id for n in neighbours])

    sample.nearest_neighbours = neighbours

    try:
        response = client.open('/api/v1/samples', method='POST', json=sample)

        assert response.status_code == 201

        sample_nodes = db.graph.nodes.match(SampleNode.__primarylabel__, name=sample.experiment_id)
        assert len(sample_nodes) == 1

        node = SampleNode.wrap(sample_nodes.first())
        if sample.nearest_neighbours:
            assert len(node.neighbours) == len(sample.nearest_neighbours)

            for neighbour in sample.nearest_neighbours:
                neighbour_nodes = [n for n in node.neighbours if n.name == neighbour.experiment_id]
                assert node.neighbours.get(neighbour_nodes[0], 'distance') == neighbour.distance
    finally:
        db.truncate()


def test_existing_neighbours_are_merged(sample_repo, db, client):
    sample_id = 'sample id'
    neighbour_id = 'neighbour id'
    neighbour_distance = 1

    sample = Sample(neighbour_id)
    sample_repo.add(sample)

    neighbour = Neighbour(neighbour_id, distance=neighbour_distance)
    sample = Sample(sample_id, nearest_neighbours=[neighbour])

    response = client.open('/api/v1/samples', method='POST', json=sample)

    assert response.status_code == 201

    neighbours = db.graph.nodes.match(SampleNode.__primarylabel__, name=neighbour_id)
    assert len(neighbours) == 1

    samples = db.graph.nodes.match(SampleNode.__primarylabel__, name=sample_id)
    assert len(samples) == 1

    relationships = db.graph.relationships.match(
        [samples.first(), neighbours.first()], NEIGHBOUR_REL_TYPE, distance=neighbour_distance)
    assert len(relationships) == 1


def test_duplicated_neighbours_are_merged(db, client):
    sample_id = 'sample id'
    neighbour_id = 'neighbour id'
    first_distance = 1
    second_distance = 2

    first_neighbour = Neighbour(neighbour_id, distance=first_distance)
    second_neighbour = Neighbour(neighbour_id, distance=second_distance)
    sample = Sample(sample_id, nearest_neighbours=[first_neighbour, second_neighbour])

    response = client.open('/api/v1/samples', method='POST', json=sample)

    assert response.status_code == 201

    neighbours = db.graph.nodes.match(SampleNode.__primarylabel__, name=neighbour_id)
    assert len(neighbours) == 1

    samples = db.graph.nodes.match(SampleNode.__primarylabel__, name=sample_id)
    assert len(samples) == 1

    relationships = db.graph.relationships.match(
        [samples.first(), neighbours.first()], NEIGHBOUR_REL_TYPE)
    assert len(relationships) == 1
    assert relationships.first()['distance'] == second_distance
