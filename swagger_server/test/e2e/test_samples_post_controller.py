from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.models import Sample
from swagger_server.test.e2e.utils import SAMPLES_API_PATH


@given(sample=from_type(Sample))
def test_create_new_sample(client, sample):
    path = str(SAMPLES_API_PATH)
    resp = client.open(path, method='POST', json=sample)
    assert resp.status_code == 201

    path = str(SAMPLES_API_PATH / sample.experiment_id)
    resp = client.open(path)
    assert resp.status_code == 200
    assert resp.json == sample.to_dict()
