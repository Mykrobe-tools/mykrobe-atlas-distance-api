from hypothesis import given, settings, assume
from hypothesis.strategies import from_type, lists

from swagger_server.models import Sample, Neighbour
from swagger_server.test.e2e.utils import SAMPLES_API_PATH, NEIGHBOURS_API_PATH


@given(sample=from_type(Sample))
@settings(max_examples=1, deadline=None)
def test_getting_neighbours_of_non_existent_sample(client, sample):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    resp = client.open(path)

    assert resp.status_code == 404
    assert resp.json['code'] == 404
    assert resp.json['message'] == 'Not found'


@given(sample=from_type(Sample))
@settings(deadline=None)
def test_getting_non_existent_neighbours(db, client, sample):
    try:
        path = str(SAMPLES_API_PATH)
        client.open(path, method='POST', json=sample)

        path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
        resp = client.open(path)
        assert resp.status_code == 404
    finally:
        db.truncate()


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id, min_size=1))
@settings(deadline=None)
def test_getting_neighbours(db, client, sample, neighbours):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])

    try:
        sample.nearest_neighbours = neighbours

        path = str(SAMPLES_API_PATH)
        client.open(path, method='POST', json=sample)

        path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
        resp = client.open(path)
        assert resp.status_code == 200

        actual = Sample.from_dict(resp.json)
        for x in sample.nearest_neighbours:
            assert x in actual.nearest_neighbours
    finally:
        db.truncate()
