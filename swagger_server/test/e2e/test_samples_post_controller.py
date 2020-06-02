from hypothesis import given, assume
from hypothesis.strategies import from_type, lists

from swagger_server.adapters.object_mappers.neo4j import SampleNode
from swagger_server.adapters.repositories.sample_repository import SampleRepository
from swagger_server.models import Sample, Neighbour


@given(sample=from_type(Sample))
def test_creating_new_sample(db, client, sample):
    try:
        response = client.open('/api/v1/samples', method='POST', json=sample)

        assert response.status_code == 201

        matcher = SampleNode.match(db.graph).where(f'_.name = "{sample.experiment_id}"')
        assert len(matcher) == 1
    finally:
        db.truncate()


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour), unique_by=lambda n: n.experiment_id))
def test_creating_sample_with_neighbours(db, client, sample, neighbours):
    assume(sample.experiment_id not in [n.experiment_id for n in neighbours])

    sample.nearest_neighbours = neighbours

    try:
        response = client.open('/api/v1/samples', method='POST', json=sample)

        assert response.status_code == 201

        matcher = SampleNode.match(db.graph).where(f'_.name = "{sample.experiment_id}"')
        assert len(matcher) == 1

        node = matcher.first()
        if sample.nearest_neighbours:
            assert len(node.neighbours) == len(sample.nearest_neighbours)

            for neighbour in sample.nearest_neighbours:
                neighbour_node = [n for n in node.neighbours if n.name == neighbour.experiment_id][0]
                assert node.neighbours.get(neighbour_node, 'distance') == neighbour.distance
    finally:
        db.truncate()


def test_creating_duplicated_sample(db, client):
    experiment_id = 'some id'
    sample = Sample(experiment_id)

    repo = SampleRepository(db)
    repo.add(sample)

    body = {
        'experiment_id': experiment_id
    }
    response = client.open('/api/v1/samples', method='POST', json=body)

    assert response.status_code == 409
    assert len(db.node_matcher.match(SampleNode.__primarylabel__, name=experiment_id)) == 1
