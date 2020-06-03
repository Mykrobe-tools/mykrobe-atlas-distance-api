from hypothesis import given, assume
from hypothesis.strategies import from_type, lists

from swagger_server.adapters.object_mappers.neo4j import SampleNode, NEIGHBOUR_REL_TYPE
from swagger_server.models import Sample, Neighbour


@given(sample=from_type(Sample))
def test_creating_new_sample(db, client, sample):
    try:
        response = client.open('/api/v1/samples', method='POST', json=sample)

        assert response.status_code == 201

        matcher = db.graph.nodes.match(SampleNode.__primarylabel__, name=sample.experiment_id)
        assert len(matcher) == 1
    finally:
        db.truncate()


def test_creating_duplicated_sample(sample_repo, db, client):
    experiment_id = 'some id'
    sample = Sample(experiment_id)
    sample_repo.add(sample)

    response = client.open('/api/v1/samples', method='POST', json=sample)

    assert response.status_code == 409
    assert len(db.graph.nodes.match(SampleNode.__primarylabel__, name=sample.experiment_id)) == 1


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour), unique_by=lambda n: n.experiment_id))
def test_creating_sample_with_neighbours(db, client, sample, neighbours):
    assume(sample.experiment_id not in [n.experiment_id for n in neighbours])

    sample.nearest_neighbours = neighbours

    try:
        response = client.open('/api/v1/samples', method='POST', json=sample)

        assert response.status_code == 201

        matcher = db.graph.nodes.match(SampleNode.__primarylabel__, name=sample.experiment_id)
        assert len(matcher) == 1

        node = SampleNode.wrap(matcher.first())
        if sample.nearest_neighbours:
            assert len(node.neighbours) == len(sample.nearest_neighbours)

            for neighbour in sample.nearest_neighbours:
                neighbour_node = [n for n in node.neighbours if n.name == neighbour.experiment_id][0]
                assert node.neighbours.get(neighbour_node, 'distance') == neighbour.distance
    finally:
        db.truncate()


def test_some_neighbours_already_exist(sample_repo, db, client):
    existing_id = 'some id'
    sample = Sample(existing_id)
    sample_repo.add(sample)

    neighbour = Neighbour(existing_id, distance=1)
    to_create = Sample('other id', nearest_neighbours=[neighbour])
    response = client.open('/api/v1/samples', method='POST', json=to_create)

    assert response.status_code == 201

    existing = db.graph.nodes.match(SampleNode.__primarylabel__, name=existing_id)
    assert len(existing) == 1

    created = db.graph.nodes.match(SampleNode.__primarylabel__, name=to_create.experiment_id)
    assert len(created) == 1

    relationship = db.graph.relationships.match(
        [created.first(), existing.first()], NEIGHBOUR_REL_TYPE, distance=neighbour.distance)
    assert len(relationship) == 1
