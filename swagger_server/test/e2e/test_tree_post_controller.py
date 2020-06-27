from hypothesis import given

from swagger_server.models import Leaf
from swagger_server.test.strategies import leaves


@given(leaf_1=leaves(), leaf_2=leaves())
def test_creating_leaves_with_existing_leaf_ids(leaf_1, leaf_2, create_leaf, sample_graph):
    leaf_2.leaf_id = leaf_1.leaf_id

    try:
        create_leaf(leaf_1, ensure=True)

        response = create_leaf(leaf_2)

        assert response.status_code == 409
        assert len(sample_graph.nodes) == 1
    finally:
        sample_graph.delete_all()


@given(leaf=leaves())
def test_creating_leaves(leaf, create_leaf, sample_graph):
    try:
        response = create_leaf(leaf)
        created = Leaf.from_dict(response.json)

        assert response.status_code == 201
        assert created == leaf
    finally:
        sample_graph.delete_all()
