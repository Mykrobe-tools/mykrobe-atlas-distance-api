from hypothesis import given
from hypothesis.strategies import text


@given(experiment_id=text())
def test_creating_new_sample(client, experiment_id):
    body = {
        'experiment_id': experiment_id
    }

    response = client.open('/api/v1/samples', method='POST', json=body)

    assert response.status_code == 201
