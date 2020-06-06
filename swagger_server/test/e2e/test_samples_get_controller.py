from hypothesis import given, settings
from hypothesis.strategies import from_type

from swagger_server.models import Sample
from swagger_server.test.e2e.utils import SAMPLES_API_PATH


@given(sample=from_type(Sample))
@settings(max_examples=1)
def test_getting_non_existent_sample(client, sample):
    path = str(SAMPLES_API_PATH / sample.experiment_id)
    resp = client.open(path)
    assert resp.status_code == 404
    assert resp.json['code'] == 404
    assert resp.json['message'] == 'Not found'