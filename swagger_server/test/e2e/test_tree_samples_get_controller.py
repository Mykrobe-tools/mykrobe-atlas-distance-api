from hypothesis import given

from swagger_server.models import Sample
from swagger_server.test.strategies import leaf_ids, trees


@given(leaf_id=leaf_ids())
def test_leaf_does_not_exist(leaf_id, get_samples_of_leaf):
    assert get_samples_of_leaf(leaf_id).status_code == 404


@given(tree=trees())
def test_get_samples(tree, create_leaf, create_sample, get_samples_of_leaf, sample_graph):
    leaf, samples = tree
    created_samples = []

    try:
        create_leaf(leaf, ensure=True)
        for sample in samples:
            if sample.nearest_neighbours:
                for neighbour in sample.nearest_neighbours:
                    create_sample(neighbour)
            resp = create_sample(sample)
            if resp.status_code == 201:
                created_samples.append(sample)

        response = get_samples_of_leaf(leaf.leaf_id)
        retrieved = [Sample.from_dict(x) for x in response.json]

        assert response.status_code == 200
        assert len(retrieved) == len(created_samples)
        for sample in retrieved:
            created = [x for x in created_samples if x.experiment_id == sample.experiment_id][0]
            assert sample.nearest_leaf_node == created.nearest_leaf_node
            assert bool(sample.nearest_neighbours) == bool(created.nearest_neighbours)
            if sample.nearest_neighbours:
                for neighbour in sample.nearest_neighbours:
                    assert neighbour in created.nearest_neighbours
    finally:
        sample_graph.delete_all()
