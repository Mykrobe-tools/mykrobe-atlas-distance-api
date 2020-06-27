from hypothesis import given

from swagger_server.models import Sample
from swagger_server.test.strategies import samples, experiment_ids, leaf_ids, leaves


@given(leaf_id=leaf_ids())
def test_getting_non_existent_leaf(leaf_id, get_leaf):
    assert get_leaf(leaf_id).status_code == 404


@given(leaf=leaves())
def test_getting_existing_sample(leaf, create_leaf, get_leaf, sample_graph):
    try:
        created = Sample.from_dict(create_leaf(leaf, ensure=True).json)
        retrieved = Sample.from_dict(get_leaf(leaf.leaf_id, ensure=True).json)

        assert created.nearest_leaf_node == retrieved.nearest_leaf_node
    finally:
        sample_graph.delete_all()
