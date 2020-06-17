from hypothesis import given, settings, assume
from hypothesis.strategies import from_type, lists, one_of, just

from swagger_server.models import Neighbour, Sample, NearestLeaf
from swagger_server.test.e2e.utils import NEIGHBOURS_API_PATH, SAMPLES_API_PATH
from swagger_server.test.strategies import full_samples


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour)))
@settings(max_examples=1)
def test_updating_neighbours_of_non_existent_sample(client, sample, neighbours):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    resp = client.open(path, method='PUT', json=neighbours)

    assert resp.status_code == 404
    assert resp.json['code'] == 404
    assert resp.json['message'] == 'Not found'


@given(sample=from_type(Sample), neighbour=from_type(Neighbour))
@settings(max_examples=1)
def test_updating_neighbours_does_not_create_new_ones(neo4j, client, sample, neighbour):
    assume(sample.experiment_id != neighbour.experiment_id)

    create_sample(sample, client)

    resp = update_neighbours(sample, [neighbour], client)
    assert resp.status_code == 200
    assert resp.json == []

    resp = get_neighbours(sample, client)
    assert resp.status_code == 404


@given(sample=full_samples())
def test_clearing_neighbours(neo4j, client, sample):
    try:
        create_sample(sample, client)

        resp = update_neighbours(sample, [], client)
        assert resp.status_code == 200
        assert resp.json == []

        resp = get_sample(sample, client)
        assert resp.status_code == 200

        resp = get_neighbours(sample, client)
        assert resp.status_code == 404
    finally:
        neo4j.truncate()


@given(sample=full_samples(), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id, min_size=1))
def test_updating_neighbours(neo4j, client, sample, neighbours):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])

    try:
        create_sample(sample, client)
        for neighbour_sample in [Sample(x.experiment_id) for x in neighbours]:
            create_sample(neighbour_sample, client)

        resp = update_neighbours(sample, neighbours, client)
        assert resp.status_code == 200
        updated = [Neighbour.from_dict(x) for x in resp.json]

        resp = get_neighbours(sample, client)
        assert resp.status_code == 200
        actual = [Neighbour.from_dict(x) for x in resp.json]

        assert len(updated) == len(actual)
        for u in updated:
            assert u in actual
    finally:
        neo4j.truncate()


def create_sample(sample, client):
    path = str(SAMPLES_API_PATH)
    return client.open(path, method='POST', json=sample)


def get_sample(sample, client):
    path = str(SAMPLES_API_PATH / sample.experiment_id)
    return client.open(path)


def update_neighbours(sample, neighbours, client):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    return client.open(path, method='PUT', json=neighbours)


def get_neighbours(sample, client):
    path = str(NEIGHBOURS_API_PATH(sample.experiment_id))
    return client.open(path)
