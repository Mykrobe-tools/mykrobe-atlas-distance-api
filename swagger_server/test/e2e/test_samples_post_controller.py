from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.models import Sample, NearestLeaf
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


@given(sample=from_type(Sample), nearest_leaf=from_type(NearestLeaf))
def test_create_new_sample_with_nearest_leaf(db, client, sample, nearest_leaf):
    try:
        sample.nearest_leaf_node = nearest_leaf

        path = str(SAMPLES_API_PATH)
        resp = client.open(path, method='POST', json=sample)
        assert resp.status_code == 201

        path = str(SAMPLES_API_PATH / sample.experiment_id)
        resp = client.open(path)
        assert resp.status_code == 200
        assert resp.json == sample.to_dict()
    finally:
        db.delete_all()
