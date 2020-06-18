import random

from hypothesis import given, assume

from swagger_server.models import Sample
from swagger_server.test.strategies import samples, neighbours


@given(sample=samples(), neighbour=neighbours())
def test_duplicated_neighbours(sample, neighbour, create_sample, sample_graph):
    assume(sample.experiment_id != neighbour.experiment_id)

    try:
        create_sample(neighbour, ensure=True)

        sample.nearest_neighbours = [neighbour, neighbour]

        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201, response.data.decode()
        assert len(created.nearest_neighbours) == 1
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_sample_existed(sample, create_sample, sample_graph):
    try:
        create_sample(sample, ensure=True)

        response = create_sample(sample)

        assert response.status_code == 409, response.data.decode()
        assert response.json['message'] == 'Already existed'
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_most_scenarios(sample, create_sample, create_leaf, sample_graph):
    neighbours_that_exist = []
    if sample.nearest_neighbours:
        neighbours_that_exist = random.sample(sample.nearest_neighbours, random.randrange(0, len(sample.nearest_neighbours)))

    try:
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)
        for neighbour in neighbours_that_exist:
            create_sample(neighbour, ensure=True)

        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created.experiment_id == sample.experiment_id
        for neighbour in sample.nearest_neighbours:
            if neighbour in neighbours_that_exist:
                assert neighbour in created.nearest_neighbours
            else:
                assert neighbour not in created.nearest_neighbours
        assert created.nearest_leaf_node == sample.nearest_leaf_node
    finally:
        sample_graph.delete_all()
