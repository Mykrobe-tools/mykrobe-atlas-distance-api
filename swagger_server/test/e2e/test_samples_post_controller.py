from hypothesis import given, assume

from swagger_server.models import Sample
from swagger_server.test.strategies import samples


@given(old=samples(), new=samples())
def test_creating_sample_with_existing_experiment_id(old, new, create_sample, sample_graph):
    try:
        create_sample(old, ensure=True)

        new.experiment_id = old.experiment_id

        response = create_sample(new)

        assert response.status_code == 409

        assert len(sample_graph.nodes) == 1
        assert len(sample_graph.relationships) == 0
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_creating_sample_with_relationships_to_non_existent_nodes(sample, create_sample, sample_graph):
    try:
        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201

        assert created.experiment_id == sample.experiment_id
        assert not created.nearest_neighbours
        assert not created.nearest_leaf_node

        assert len(sample_graph.nodes) == 1
        assert len(sample_graph.relationships) == 0
    finally:
        sample_graph.delete_all()


@given(sample=samples(has_neighbours=True))
def test_duplicated_neighbour_relationships_are_not_created(sample, create_sample, sample_graph):
    assume(sample.experiment_id not in [x.experiment_id for x in sample.nearest_neighbours])

    unique_neighbour_ids = set([x.experiment_id for x in sample.nearest_neighbours])

    try:
        for neighbour in sample.nearest_neighbours:
            create_sample(neighbour)

        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert len(created.nearest_neighbours) == len(unique_neighbour_ids)
        assert len(sample_graph.relationships) == len(unique_neighbour_ids)
    finally:
        sample_graph.delete_all()


@given(sample=samples(has_neighbours=True, unique_neighbours=True))
def test_self_neighbouring_relationships_are_not_created(sample, create_sample, sample_graph):
    valid_neighbours = [x for x in sample.nearest_neighbours if x.experiment_id != sample.experiment_id]

    try:
        for neighbour in valid_neighbours:
            create_sample(neighbour, ensure=True)

        response = create_sample(sample, ensure=True)
        created = Sample.from_dict(response.json)

        assert len(created.nearest_neighbours) == len(valid_neighbours)
        assert len(sample_graph.relationships) == len(valid_neighbours)
    finally:
        sample_graph.delete_all()


@given(sample=samples())
def test_created_sample_matches_retrieved_sample(sample, create_sample, create_leaf, get_sample, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                if neighbour.experiment_id != sample.experiment_id:
                    create_sample(neighbour)
        if sample.nearest_leaf_node:
            create_leaf(sample.nearest_leaf_node, ensure=True)

        created = Sample.from_dict(create_sample(sample, ensure=True).json)
        retrieved = Sample.from_dict(get_sample(sample, ensure=True).json)

        assert created.nearest_leaf_node == retrieved.nearest_leaf_node
        assert len(created.nearest_neighbours) == len(retrieved.nearest_neighbours)
        for neighbour in created.nearest_neighbours:
            assert neighbour in retrieved.nearest_neighbours
    finally:
        sample_graph.delete_all()
