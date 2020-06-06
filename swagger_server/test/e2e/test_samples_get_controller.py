from hypothesis import given, settings, assume
from hypothesis.strategies import from_type, lists

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.test.e2e.utils import SAMPLES_API_PATH


@given(sample=from_type(Sample))
@settings(max_examples=1)
def test_getting_non_existent_sample(client, sample):
    path = str(SAMPLES_API_PATH / sample.experiment_id)
    resp = client.open(path)
    assert resp.status_code == 404
    assert resp.json['code'] == 404
    assert resp.json['message'] == 'Not found'


@given(sample=from_type(Sample), nearest_leaf=from_type(NearestLeaf), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id))
def test_getting_sample(db, client, sample, nearest_leaf, neighbours):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])

    try:
        sample.nearest_leaf_node = nearest_leaf
        sample.nearest_neighbours = neighbours

        path = str(SAMPLES_API_PATH)
        client.open(path, method='POST', json=sample)

        path = str(SAMPLES_API_PATH / sample.experiment_id)
        resp = client.open(path)
        assert resp.status_code == 200

        actual = Sample.from_dict(resp.json)
        assert actual.experiment_id == sample.experiment_id
        assert actual.nearest_leaf_node == sample.nearest_leaf_node
        assert bool(actual.nearest_neighbours) == bool(sample.nearest_neighbours)

        if sample.nearest_neighbours and actual.nearest_neighbours:
            for x in sample.nearest_neighbours:
                assert x in actual.nearest_neighbours
    finally:
        db.delete_all()