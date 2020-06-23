from hypothesis import given

from swagger_server.test.strategies import samples


@given(sample=samples())
def test_deleting_non_existent_samples(sample, delete_sample):
    assert delete_sample(sample).status_code == 404


@given(sample=samples())
def test_deleting_existing_samples(sample, create_sample, create_leaf, delete_sample, get_sample, get_leaf, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour, ensure=True)
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)

        create_sample(sample, ensure=True)

        response = delete_sample(sample)
        assert response.status_code == 200

        assert get_sample(sample).status_code == 404
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                assert get_sample(neighbour, ensure=True)
        if sample.nearest_leaf_node:
            get_leaf(sample.nearest_leaf_node, ensure=True)
    finally:
        sample_graph.delete_all()
