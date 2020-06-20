from hypothesis import given, assume, settings, HealthCheck
from pytest import fixture

from swagger_server.models import Sample
from swagger_server.test.strategies import samples


class TestSampleExists:
    @fixture(scope='class')
    def existing_sample(self, create_sample, sample_graph):
        sample = Sample('0')
        create_sample(sample, ensure=True)
        yield sample
        sample_graph.delete_all()

    @given(sample=samples())
    def test_endpoint_returns_409(self, sample, existing_sample, create_sample):
        sample.experiment_id = existing_sample.experiment_id

        response = create_sample(existing_sample)

        assert response.status_code == 409, response.data.decode()

    @given(sample=samples())
    def test_nothing_is_created(self, sample, existing_sample, create_sample, sample_graph):
        sample.experiment_id = existing_sample.experiment_id

        create_sample(sample)

        assert len(sample_graph.nodes) == 1
        assert len(sample_graph.relationships) == 0


class TestLeafAndNeighboursDoNotExist:
    @given(sample=samples())
    def test_sample_is_created(self, sample, create_sample, sample_graph):
        try:
            response = create_sample(sample)
            created = Sample.from_dict(response.json)

            assert response.status_code == 201, response.data.decode()
            assert created.experiment_id == sample.experiment_id

            assert len(sample_graph.nodes) == 1
        finally:
            sample_graph.delete_all()

    @given(sample=samples())
    def test_relationships_are_not_created(self, sample, create_sample, sample_graph):
        try:
            response = create_sample(sample, ensure=True)
            created = Sample.from_dict(response.json)

            assert not created.nearest_neighbours
            assert not created.nearest_leaf_node

            assert len(sample_graph.relationships) == 0
        finally:
            sample_graph.delete_all()


class TestLeafAndNeighboursExist:
    @given(sample=samples(unique_neighbours=True))
    @settings(suppress_health_check=(HealthCheck.filter_too_much,))
    def test_relationships_are_created(self, sample, create_sample, create_leaf, sample_graph):
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
    def test_duplicated_neighbour_relationships_are_not_created(self, sample, create_sample, sample_graph):
        assume(sample.nearest_neighbours)

        unique_neighbour_ids = set([x.experiment_id for x in sample.nearest_neighbours])

        assume(sample.experiment_id not in unique_neighbour_ids)

        try:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour)

            response = create_sample(sample, ensure=True)
            created = Sample.from_dict(response.json)

            assert len(created.nearest_neighbours) == len(unique_neighbour_ids)
            assert len(sample_graph.relationships) == len(unique_neighbour_ids)
        finally:
            sample_graph.delete_all()

    @given(sample=samples(unique_neighbours=True))
    def test_self_neighbouring_relationships_are_not_created(self, sample, create_sample, sample_graph):
        assume(sample.nearest_neighbours)

        valid_neighbour_ids = [x.experiment_id for x in sample.nearest_neighbours if x.experiment_id != sample.experiment_id]

        try:
            for neighbour in sample.nearest_neighbours:
                if neighbour.experiment_id in valid_neighbour_ids:
                    create_sample(neighbour, ensure=True)

            response = create_sample(sample, ensure=True)
            created = Sample.from_dict(response.json)

            assert len(created.nearest_neighbours) == len(valid_neighbour_ids)
            assert len(sample_graph.relationships) == len(valid_neighbour_ids)
        finally:
            sample_graph.delete_all()
