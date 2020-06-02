from hypothesis import given
from hypothesis.strategies import text

from swagger_server.adapters.object_mappers.neo4j import SampleNode
from swagger_server.adapters.repositories.sample_repository import SampleRepository
from swagger_server.models import Sample


@given(experiment_id=text())
def test_creating_new_sample(db, client, experiment_id):
    try:
        body = {
            'experiment_id': experiment_id
        }

        response = client.open('/api/v1/samples', method='POST', json=body)

        assert response.status_code == 201
        assert len(db.node_matcher.match(SampleNode.__primarylabel__, name=experiment_id)) == 1
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
