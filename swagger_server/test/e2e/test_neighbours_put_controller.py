import random

from hypothesis import given, assume
from hypothesis.strategies import lists

from swagger_server.models import Neighbour, NearestLeaf
from swagger_server.test.strategies import neighbours, experiment_ids, samples


@given(experiment_id=experiment_ids(), new_neighbours=lists(neighbours()))
def test_updating_neighbours_of_non_existent_samples(experiment_id, new_neighbours, update_neighbours, sample_graph):
    assert update_neighbours(experiment_id, new_neighbours).status_code == 404


@given(sample=samples(), new_neighbours=lists(neighbours(), unique_by=lambda x: x.experiment_id))
def test_updating_ensures_a_sample_neighbours_set_to_be_the_new_one(sample, new_neighbours, create_sample, update_neighbours, sample_graph):
    assume(sample.experiment_id not in [x.experiment_id for x in new_neighbours])

    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour)
        create_sample(sample, ensure=True)

        existing_neighbours = []
        if new_neighbours:
            existing_neighbours = random.sample(new_neighbours, random.randrange(0, len(new_neighbours)))
            for neighbour in existing_neighbours:
                create_sample(neighbour)

        response = update_neighbours(sample.experiment_id, new_neighbours)
        updated_neighbours = [Neighbour.from_dict(x) for x in response.json]

        assert response.status_code == 200
        assert len(updated_neighbours) == len(existing_neighbours)
        for neighbour in existing_neighbours:
            assert neighbour in updated_neighbours
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_clear_neighbours(sample, create_sample, update_neighbours, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour)
        create_sample(sample, ensure=True)

        response = update_neighbours(sample.experiment_id, [])
        updated_neighbours = [Neighbour.from_dict(x) for x in response.json]

        assert response.status_code == 200
        assert not updated_neighbours
    finally:
        sample_graph.delete_all()


@given(sample=samples(must_have_leaf=True), new_neighbours=lists(neighbours()))
def test_updating_never_touches_lineages(sample, new_neighbours, create_sample, update_neighbours, create_leaf,
                                         get_nearest_leaf, sample_graph):
    try:
        create_leaf(sample.nearest_leaf_node)

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour)
        create_sample(sample, ensure=True)

        if new_neighbours:
            for neighbour in new_neighbours:
                create_sample(neighbour)
        update_neighbours(sample.experiment_id, new_neighbours, ensure=True)

        leaf = NearestLeaf.from_dict(get_nearest_leaf(sample.experiment_id, ensure=True).json)

        assert leaf == sample.nearest_leaf_node
    finally:
        sample_graph.delete_all()
