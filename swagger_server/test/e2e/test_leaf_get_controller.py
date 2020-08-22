from hypothesis import given

from swagger_server.models import NearestLeaf
from swagger_server.test.strategies import samples, experiment_ids


@given(experiment_id=experiment_ids())
def test_getting_leaf_of_non_existent_sample(experiment_id, get_nearest_leaf):
    assert get_nearest_leaf(experiment_id).status_code == 404


@given(sample=samples())
def test_getting_non_existent_leaf(sample, create_sample, get_nearest_leaf, sample_graph):
    try:
        create_sample(sample, ensure=True)

        assert get_nearest_leaf(sample.experiment_id).status_code == 404
    finally:
        sample_graph.delete_all()


@given(sample=samples(must_have_leaf=True))
def test_getting_leaf_of_existing_sample(sample, create_sample, create_leaf, get_nearest_leaf, sample_graph):
    try:
        create_leaf(sample.nearest_leaf_node, ensure=True)
        create_sample(sample, ensure=True)

        response = get_nearest_leaf(sample.experiment_id)
        retrieved = NearestLeaf.from_dict(response.json)

        assert response.status_code == 200
        assert retrieved == sample.nearest_leaf_node
    finally:
        sample_graph.delete_all()
