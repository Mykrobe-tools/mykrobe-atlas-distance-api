from hypothesis import given

from swagger_server.test.strategies import samples, experiment_ids


@given(experiment_id=experiment_ids())
def test_deleting_non_existent_samples(experiment_id, delete_sample):
    assert delete_sample(experiment_id).status_code == 404


@given(sample=samples())
def test_deleting_existing_samples(sample, create_sample, create_leaf, delete_sample, get_sample, get_leaf, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour, ensure=True)
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)

        create_sample(sample, ensure=True)

        response = delete_sample(sample.experiment_id)
        assert response.status_code == 204

        assert get_sample(sample.experiment_id).status_code == 404
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                assert get_sample(neighbour.experiment_id, ensure=True)
        if sample.nearest_leaf_node:
            get_leaf(sample.nearest_leaf_node.leaf_id, ensure=True)
    finally:
        sample_graph.delete_all()
