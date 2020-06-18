from hypothesis import given, assume, settings

from swagger_server.models import Sample
from swagger_server.test.strategies import samples, neighbours


@given(sample=samples(), neighbour=neighbours())
@settings(max_examples=1)
def test_endpoint_deduplicates_neighbour_relationships(sample, neighbour, create_sample, sample_graph):
    assume(sample.experiment_id != neighbour.experiment_id)

    try:
        create_sample(neighbour, ensure=True)

        sample.nearest_neighbours = [neighbour, neighbour]

        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201, response.data.decode()
        assert len(created.nearest_neighbours) == 1
    finally:
        sample_graph.delete_all()


@given(sample=samples())
@settings(max_examples=1)
def test_endpoint_returns_409_on_duplicated_sample(sample, create_sample, sample_graph):
    try:
        create_sample(sample, ensure=True)

        response = create_sample(sample)

        assert response.status_code == 409, response.data.decode()
        assert response.json['message'] == 'Already existed'
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_endpoint_creates_non_existent_sample_and_relationships_with_existing_nodes(sample, create_sample, create_leaf, sample_graph):
    assume(sample.nearest_leaf_node)

    try:
        create_leaf(sample.nearest_leaf_node, ensure=True)
        for neighbour in sample.nearest_neighbours:
            create_sample(neighbour, ensure=True)

        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created == sample
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_endpoint_does_not_create_new_leaves_and_neighbour_nodes(sample, create_sample, create_leaf, sample_graph):
    try:
        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created.experiment_id == sample.experiment_id
        assert not created.nearest_neighbours
        assert not created.nearest_leaf_node
    finally:
        sample_graph.delete_all()
