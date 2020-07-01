from hypothesis import given

from swagger_server.models import Sample
from swagger_server.test.strategies import samples, experiment_ids


@given(experiment_id=experiment_ids())
def test_non_existent_samples(experiment_id, delete_nearest_leaf):
    assert delete_nearest_leaf(experiment_id).status_code == 404


@given(sample=samples())
def test_non_existent_leaves(sample, create_sample, delete_nearest_leaf, sample_graph):
    try:
        create_sample(sample)

        assert delete_nearest_leaf(sample.experiment_id).status_code == 204
    finally:
        sample_graph.delete_all()


@given(sample=samples(must_have_leaf=True))
def test_deleting_nearest_leaves(sample, create_sample, create_leaf, delete_nearest_leaf, get_sample, sample_graph):
    try:
        create_leaf(sample.nearest_leaf_node, ensure=True)

        create_sample(sample, ensure=True)

        response = delete_nearest_leaf(sample.experiment_id)
        assert response.status_code == 204

        retrieved = Sample.from_dict(get_sample(sample.experiment_id, ensure=True).json)
        assert not retrieved.nearest_leaf_node
    finally:
        sample_graph.delete_all()
