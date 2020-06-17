from hypothesis import given, settings, assume
from hypothesis.strategies import from_type, lists, one_of, just

from swagger_server.models import Neighbour, Sample, NearestLeaf
from swagger_server.test.e2e.utils import NEIGHBOURS_API_PATH, SAMPLES_API_PATH


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour)))
@settings(max_examples=1)
def test_updating_neighbours_of_non_existent_sample(client, sample, neighbours):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    resp = client.open(path, method='PUT', json=neighbours)

    assert resp.status_code == 404
    assert resp.json['code'] == 404
    assert resp.json['message'] == 'Not found'


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id),
       nearest_leaf=one_of(just(None), from_type(NearestLeaf)))
def test_updating_neighbours(neo4j, client, sample, neighbours, nearest_leaf):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])

    try:
        sample.nearest_leaf_node = nearest_leaf
        create_sample(sample, client)

        resp = update_neighbours(sample, neighbours, client)
        assert resp.status_code == 200

        updated_neighbours = [Neighbour.from_dict(n) for n in resp.json]
        assert updated_neighbours == neighbours

        resp = get_neighbours(sample, client)
        if not neighbours:
            assert resp.status_code == 404
        else:
            actual_neighbours = [Neighbour.from_dict(x) for x in resp.json]
            assert len(actual_neighbours) == len(neighbours)
            for x in neighbours:
                assert x in actual_neighbours
    finally:
        neo4j.truncate()


def create_sample(sample, client):
    path = str(SAMPLES_API_PATH)
    client.open(path, method='POST', json=sample)


def update_neighbours(sample, neighbours, client):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    return client.open(path, method='PUT', json=neighbours)


def get_neighbours(sample, client):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    return client.open(path)
