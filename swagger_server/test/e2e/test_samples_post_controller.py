import random

from hypothesis import given

from swagger_server.models import Sample, Neighbour
from swagger_server.test.strategies import samples, experiment_ids, distances


@given(sample=samples(), neighbour_id=experiment_ids(), d1=distances(), d2=distances())
def test_creating_samples_with_multiple_distances_to_one_neighbour(sample, neighbour_id, d1, d2, create_sample, sample_graph):
    sample.nearest_neighbours = [
        Neighbour(neighbour_id, d1),
        Neighbour(neighbour_id, d2)
    ]

    assert create_sample(sample).status_code == 400

    assert len(sample_graph.nodes) == 0


@given(sample_1=samples(), sample_2=samples())
def test_creating_samples_with_existing_experiment_ids(sample_1, sample_2, create_sample, sample_graph):
    sample_2.experiment_id = sample_1.experiment_id

    try:
        create_sample(sample_1, ensure=True)

        response = create_sample(sample_2)

        assert response.status_code == 409
        assert len(sample_graph.nodes) == 1
    finally:
        sample_graph.delete_all()


@given(sample=samples(must_have_neighbours=True, must_have_leaf=True))
def test_only_relationships_to_existing_nodes_are_created(sample, create_sample, create_leaf, get_sample, sample_graph):
    existing_neighbours = random.sample(sample.nearest_neighbours, random.randrange(0, len(sample.nearest_neighbours)))

    try:
        for neighbour in existing_neighbours:
            create_sample(neighbour, ensure=True)
        create_leaf(sample.nearest_leaf_node, ensure=True)

        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created.experiment_id == sample.experiment_id
        assert created.nearest_leaf_node == sample.nearest_leaf_node
        assert len(created.nearest_neighbours) == len(existing_neighbours)
        for neighbour in existing_neighbours:
            assert neighbour in created.nearest_neighbours

        retrieved = Sample.from_dict(get_sample(sample.experiment_id, ensure=True).json)
        assert created.nearest_leaf_node == retrieved.nearest_leaf_node
        assert len(created.nearest_neighbours) == len(retrieved.nearest_neighbours)
        for neighbour in created.nearest_neighbours:
            assert neighbour in retrieved.nearest_neighbours
    finally:
        sample_graph.delete_all()
