from copy import deepcopy

from hypothesis import given, assume
from hypothesis.strategies import from_type, lists, integers

from swagger_server.models import Sample, NearestLeaf, Neighbour
from swagger_server.test.e2e.utils import SAMPLES_API_PATH


@given(sample=from_type(Sample))
def test_create_new_sample(client, sample):
    check_create_and_retrieve_sample(sample, client)


@given(sample=from_type(Sample), nearest_leaf=from_type(NearestLeaf))
def test_create_new_sample_with_nearest_leaf(db, client, sample, nearest_leaf):
    try:
        sample.nearest_leaf_node = nearest_leaf
        check_create_and_retrieve_sample(sample, client)
    finally:
        db.delete_all()


@given(sample=from_type(Sample), neighbour=from_type(Neighbour))
def test_create_new_sample_with_one_neighbour(db, client, sample, neighbour):
    try:
        sample.nearest_neighbours = [neighbour]
        check_create_and_retrieve_sample(sample, client)
    finally:
        db.delete_all()


@given(sample=from_type(Sample), neighbours=lists(from_type(Neighbour), unique_by=lambda x: x.experiment_id))
def test_create_new_sample_with_multiple_unique_neighbours(db, client, sample, neighbours):
    assume(sample.experiment_id not in [x.experiment_id for x in neighbours])
    try:
        sample.nearest_neighbours = neighbours
        check_create_and_retrieve_sample(sample, client)
    finally:
        db.delete_all()


@given(sample=from_type(Sample), distance=integers())
def test_create_new_sample_that_neighbour_itself(db, client, sample, distance):
    try:
        sample.nearest_neighbours = [Neighbour(sample.experiment_id, distance)]
        check_create_and_retrieve_sample(sample, client)
    finally:
        db.delete_all()


def check_create_and_retrieve_sample(sample, client):
    path = str(SAMPLES_API_PATH)
    resp = client.open(path, method='POST', json=sample)
    assert resp.status_code == 201

    path = str(SAMPLES_API_PATH / sample.experiment_id)
    resp = client.open(path)
    assert resp.status_code == 200

    actual = Sample.from_dict(resp.json)
    expected = deepcopy(sample)
    expected.nearest_neighbours = [x for x in expected.nearest_neighbours if x.experiment_id != expected.experiment_id]

    assert actual.experiment_id == expected.experiment_id
    assert actual.nearest_leaf_node == expected.nearest_leaf_node
    assert bool(actual.nearest_neighbours) == bool(expected.nearest_neighbours)

    if expected.nearest_neighbours:
        for x in expected.nearest_neighbours:
            if x.experiment_id != sample.experiment_id:
                assert x in actual.nearest_neighbours
            else:
                assert x not in actual.nearest_neighbours