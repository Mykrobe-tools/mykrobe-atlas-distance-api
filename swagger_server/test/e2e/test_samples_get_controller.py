from hypothesis import given

from swagger_server.models import Sample
from swagger_server.test.strategies import samples, experiment_ids


@given(experiment_id=experiment_ids())
def test_getting_non_existent_sample(experiment_id, get_sample):
    assert get_sample(experiment_id).status_code == 404


@given(sample=samples())
def test_getting_existing_sample(sample, create_sample, create_leaf, get_sample, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour, ensure=True)
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)

        created = Sample.from_dict(create_sample(sample, ensure=True).json)
        retrieved = Sample.from_dict(get_sample(sample.experiment_id, ensure=True).json)

        assert created.nearest_leaf_node == retrieved.nearest_leaf_node
        assert len(created.nearest_neighbours) == len(retrieved.nearest_neighbours)
        for neighbour in created.nearest_neighbours:
            assert neighbour in retrieved.nearest_neighbours
    finally:
        sample_graph.delete_all()
