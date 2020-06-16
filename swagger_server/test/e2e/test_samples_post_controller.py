from hypothesis import given, assume, settings
from hypothesis.strategies import from_type, lists, integers

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.test.e2e.utils import SAMPLES_API_PATH


@given(sample=from_type(Sample), nearest_leaf=from_type(NearestLeaf), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id))
def test_create_new_sample(neo4j, client, sample, nearest_leaf, neighbours):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])

    try:
        sample.nearest_leaf_node = nearest_leaf
        sample.nearest_neighbours = neighbours

        actual = create_and_retrieve_sample(sample, client)

        assert actual.experiment_id == sample.experiment_id
        assert actual.nearest_leaf_node == sample.nearest_leaf_node
        assert bool(actual.nearest_neighbours) == bool(sample.nearest_neighbours)

        if sample.nearest_neighbours and actual.nearest_neighbours:
            for x in sample.nearest_neighbours:
                assert x in actual.nearest_neighbours
    finally:
        neo4j.truncate()


@given(sample=from_type(Sample), distance=integers())
@settings(max_examples=1)
def test_create_new_sample_that_neighbour_itself(neo4j, client, sample, distance):
    sample.nearest_neighbours = [Neighbour(sample.experiment_id, distance)]

    actual = create_and_retrieve_sample(sample, client)

    assert not actual.nearest_neighbours


@given(sample=from_type(Sample), neighbour=from_type(Neighbour))
@settings(max_examples=1)
def test_create_new_sample_with_duplicated_neighbours(neo4j, client, sample, neighbour):
    assume(sample.experiment_id != neighbour.experiment_id)

    sample.nearest_neighbours = [neighbour, neighbour]

    actual = create_and_retrieve_sample(sample, client)

    assert len(actual.nearest_neighbours) == 1
    assert actual.nearest_neighbours[0] == neighbour


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour)), nearest_leaf=from_type(NearestLeaf))
def test_create_existing_sample(neo4j, client, sample, neighbours, nearest_leaf):
    try:
        sample.nearest_neighbours = neighbours
        sample.nearest_leaf_node = nearest_leaf

        path = str(SAMPLES_API_PATH)
        resp = client.open(path, method='POST', json=sample)
        assert resp.status_code == 201

        resp = client.open(path, method='POST', json=sample)
        assert resp.status_code == 409
        assert resp.json['code'] == 409
        assert resp.json['message'] == 'Already existed'
    finally:
        neo4j.truncate()


def create_and_retrieve_sample(sample, client):
    path = str(SAMPLES_API_PATH)
    resp = client.open(path, method='POST', json=sample)
    assert resp.status_code == 201

    path = str(SAMPLES_API_PATH / sample.experiment_id)
    resp = client.open(path)
    assert resp.status_code == 200

    return Sample.from_dict(resp.json)
