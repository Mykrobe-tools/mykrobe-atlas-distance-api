from hypothesis import given

from swagger_server.models import Sample
from swagger_server.test.strategies import samples


@given(sample=samples())
def test_creating_first_sample(sample, create_sample, sample_graph):
    try:
        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created.experiment_id == sample.experiment_id
        assert not created.nearest_neighbours
        assert not created.nearest_leaf_node
    finally:
        sample_graph.delete_all()
