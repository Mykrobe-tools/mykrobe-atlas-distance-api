from hypothesis import given, assume

from swagger_server.models import Sample
from swagger_server.test.strategies import samples


@given(sample=samples())
def test_endpoint_returns_404_if_the_sample_does_not_exist(sample, get_sample):
    assert get_sample(sample).status_code == 404


@given(sample=samples(has_neighbours=True, unique_neighbours=True, has_leaf=True))
def test_endpoint_returns_the_sample_and_its_relationships_if_they_exist(sample, get_sample, create_sample, create_leaf, sample_graph):
    assume(sample.experiment_id not in [x.experiment_id for x in sample.nearest_neighbours])

    try:
        for neighbour in sample.nearest_neighbours:
            create_sample(neighbour, ensure=True)
        create_leaf(sample.nearest_leaf_node)
        create_sample(sample, ensure=True)

        response = get_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 200
        assert created.experiment_id == sample.experiment_id
        assert created.nearest_leaf_node == sample.nearest_leaf_node
        assert len(created.nearest_neighbours) == len(sample.nearest_neighbours)
        for neighbour in created.nearest_neighbours:
            assert neighbour in sample.nearest_neighbours
    finally:
        sample_graph.delete_all()
