from hypothesis import given, settings, assume
from hypothesis.strategies import from_type, lists

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.test.e2e.utils import SAMPLES_API_PATH


@given(sample=from_type(Sample))
@settings(max_examples=1)
def test_deleting_non_existent_sample(client, sample):
    path = str(SAMPLES_API_PATH / sample.experiment_id)
    resp = client.open(path, method='DELETE')

    assert resp.status_code == 404
    assert resp.json['code'] == 404
    assert resp.json['message'] == 'Not found'


@given(sample=from_type(Sample), nearest_leaf=from_type(NearestLeaf), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id))
def test_deleting_sample(db, client, sample, nearest_leaf, neighbours):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])

    try:
        sample.nearest_leaf_node = nearest_leaf
        sample.nearest_neighbours = neighbours

        path = str(SAMPLES_API_PATH)
        client.open(path, method='POST', json=sample)

        path = str(SAMPLES_API_PATH / sample.experiment_id)
        resp = client.open(path, method='DELETE')
        assert resp.status_code == 200

        path = str(SAMPLES_API_PATH / sample.experiment_id)
        resp = client.open(path)
        assert resp.status_code == 404
    finally:
        db.delete_all()