from hypothesis import given, assume, settings, HealthCheck

from swagger_server.models import Sample
from swagger_server.test.strategies import samples, neighbours


@given(old=samples(), new=samples())
def test_nothing_is_created_if_sample_experiment_id_exists(old, new, create_sample, sample_graph):
    try:
        create_sample(old, ensure=True)
        new.experiment_id = old.experiment_id

        response = create_sample(new)

        assert response.status_code == 409, response.data.decode()
        assert response.json['message'] == 'Already existed'

        assert len(sample_graph.nodes) == 1
        assert len(sample_graph.relationships) == 0
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_sample_is_created_if_experiment_id_does_not_exist(sample, create_sample, get_sample, sample_graph):
    try:
        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201, response.data.decode()
        assert created.experiment_id == sample.experiment_id

        assert get_sample(sample).status_code == 200
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_relationships_with_non_existent_leaves_and_neighbours_are_not_created(sample, create_sample, sample_graph):
    try:
        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert not created.nearest_neighbours
        assert not created.nearest_leaf_node

        assert len(sample_graph.nodes) == 1
        assert len(sample_graph.relationships) == 0
    finally:
        sample_graph.delete_all()


@given(sample=samples(unique_neighbours=True))
@settings(suppress_health_check=(HealthCheck.filter_too_much,))
def test_relationships_with_existing_leaves_and_neighbours_are_created(sample, create_sample, create_leaf, sample_graph):
    assume(sample.nearest_leaf_node)
    assume(sample.nearest_neighbours)
    assume(sample.experiment_id not in [x.experiment_id for x in sample.nearest_neighbours])

    try:
        for neighbour in sample.nearest_neighbours:
            create_sample(neighbour, ensure=True)
        create_leaf(sample.nearest_leaf_node, ensure=True)

        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert created.nearest_neighbours == sample.nearest_neighbours
        assert created.nearest_leaf_node == sample.nearest_leaf_node

        assert len(sample_graph.nodes) == len(created.nearest_neighbours) + 2
        assert len(sample_graph.relationships) == len(created.nearest_neighbours) + 1
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_duplicated_neighbour_relationships_are_not_created(sample, create_sample, sample_graph):
    assume(sample.nearest_neighbours)

    unique_neighbours = []
    for neighbour in sample.nearest_neighbours:
        if neighbour.experiment_id not in [x.experiment_id for x in unique_neighbours]:
            unique_neighbours.append(neighbour)

    assume(sample.experiment_id not in [x.experiment_id for x in unique_neighbours])

    try:
        for neighbour in unique_neighbours:
            create_sample(neighbour, ensure=True)

        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert len(created.nearest_neighbours) == len(unique_neighbours)

        assert len(sample_graph.nodes) == len(unique_neighbours) + 1
        assert len(sample_graph.relationships) == len(unique_neighbours)
    finally:
        sample_graph.delete_all()


@given(sample=samples(), neighbour=neighbours())
def test_self_neighbouring_relationships_are_not_created(sample, neighbour, create_sample, sample_graph):
    neighbour.experiment_id = sample.experiment_id
    sample.nearest_neighbours = [neighbour]

    try:
        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert neighbour not in created.nearest_neighbours

        assert len(sample_graph.nodes) == 1
        assert len(sample_graph.relationships) == 0
    finally:
        sample_graph.delete_all()
