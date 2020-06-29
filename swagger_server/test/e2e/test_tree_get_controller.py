from hypothesis import given

from swagger_server.models import Leaf
from swagger_server.test.strategies import leaf_ids, leaves


@given(leaf_id=leaf_ids())
def test_getting_non_existent_leaves(leaf_id, get_leaf):
    assert get_leaf(leaf_id).status_code == 404


@given(leaf=leaves())
def test_getting_existing_leaves(leaf, create_leaf, get_leaf, sample_graph):
    try:
        created = Leaf.from_dict(create_leaf(leaf, ensure=True).json)
        retrieved = Leaf.from_dict(get_leaf(leaf.leaf_id, ensure=True).json)

        assert created == retrieved
    finally:
        sample_graph.delete_all()
