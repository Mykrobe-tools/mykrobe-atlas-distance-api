from hypothesis import given

from swagger_server.test.strategies import leaf_ids, leaves


@given(leaf_id=leaf_ids())
def test_deleting_non_existent_leaves(leaf_id, delete_leaf):
    assert delete_leaf(leaf_id).status_code == 404


@given(leaf=leaves())
def test_deleting_existing_leaves(leaf, create_leaf, delete_leaf, get_leaf, sample_graph):
    try:
        create_leaf(leaf, ensure=True)

        response = delete_leaf(leaf.leaf_id)
        assert response.status_code == 200

        assert get_leaf(leaf.leaf_id).status_code == 404
    finally:
        sample_graph.delete_all()
