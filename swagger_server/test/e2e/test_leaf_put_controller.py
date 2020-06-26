from hypothesis import given
from pytest import skip

from swagger_server.models import NearestLeaf
from swagger_server.test.strategies import experiment_ids, samples, nearest_leaves


@given(experiment_id=experiment_ids(), nearest_leaf=nearest_leaves())
def test_updating_leaf_of_non_existent_samples(experiment_id, nearest_leaf, update_nearest_leaf, sample_graph):
    response = update_nearest_leaf(experiment_id, nearest_leaf)
    assert response.status_code == 404, response.data.decode()


@given(sample=samples(), nearest_leaf=nearest_leaves())
def test_updating_ensures_a_sample_lineage_to_be_the_new_one(sample, nearest_leaf, create_leaf, create_sample, update_nearest_leaf, sample_graph):
    try:
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)
        create_sample(sample, ensure=True)

        if nearest_leaf:
            create_leaf(nearest_leaf)

        response = update_nearest_leaf(sample.experiment_id, nearest_leaf)
        updated_leaf = NearestLeaf.from_dict(response.json)

        assert response.status_code == 200
        assert updated_leaf == nearest_leaf
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_clear_leaf(sample, create_leaf, create_sample, update_nearest_leaf, sample_graph):
    skip('need spec update')

    try:
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)
        create_sample(sample, ensure=True)

        response = update_nearest_leaf(sample.experiment_id, None)
        updated_leaf = NearestLeaf.from_dict(response.json)

        assert response.status_code == 200
        assert not updated_leaf
    finally:
        sample_graph.delete_all()
