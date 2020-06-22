from hypothesis import given

from swagger_server.models import Sample
from swagger_server.test.strategies import samples


@given(sample=samples())
def test_getting_non_existent_sample(sample, get_sample):
    assert get_sample(sample).status_code == 404


@given(sample=samples())
def test_retrieved_sample_matches_created_sample(sample, create_sample, create_leaf, get_sample, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                if neighbour.experiment_id != sample.experiment_id:
                    create_sample(neighbour)
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)

        created = Sample.from_dict(create_sample(sample, ensure=True).json)
        retrieved = Sample.from_dict(get_sample(sample, ensure=True).json)

        assert created.nearest_leaf_node == retrieved.nearest_leaf_node
        assert len(created.nearest_neighbours) == len(retrieved.nearest_neighbours)
        for neighbour in created.nearest_neighbours:
            assert neighbour in retrieved.nearest_neighbours
    finally:
        sample_graph.delete_all()
