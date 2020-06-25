import logging

import connexion
from flask import g
from hypothesis import settings
from py2neo import Graph
from pytest import fixture

from swagger_server.encoder import JSONEncoder
from swagger_server.factories import NearestLeafFactory
from swagger_server.ogm import LeafNode, SampleNode


@fixture(scope='session')
def sample_graph():
    repo = Graph()
    yield repo
    repo.delete_all()


@fixture(scope='session')
def app(sample_graph):
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../../openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('openapi.yaml')

    with app.app.app_context():
        g.sample_graph = sample_graph
        yield app.app


@fixture(scope='session')
def client(app):
    with app.test_client() as client:
        yield client


@fixture
def make_request(client):
    def request(path, method, json=None, ensure=False, success_code=200):
        response = client.open(path, method=method, json=json)
        if ensure:
            assert response.status_code == success_code, f'{response.data.decode()}\nPath: {path}\nMethod: {method}\nBody: {json}'
        return response
    return request


API_ROOT = '/api/v1'


@fixture
def create_sample(make_request):
    def request(sample, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples', 'POST', sample, success_code=201, *args, **kwargs)
    return request


@fixture
def get_sample(make_request):
    def request(experiment_id, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{experiment_id}', 'GET', *args, **kwargs)
    return request


@fixture
def delete_sample(make_request):
    def request(experiment_id):
        return make_request(f'{API_ROOT}/samples/{experiment_id}', 'DELETE')
    return request


@fixture
def get_neighbours(make_request):
    def request(experiment_id, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{experiment_id}/nearest-neighbours', 'GET', *args, **kwargs)
    return request


@fixture
def update_neighbours(make_request):
    def request(experiment_id, neighbours, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{experiment_id}/nearest-neighbours', 'PUT', neighbours, *args, **kwargs)
    return request


# TODO: Replace with endpoint request
@fixture
def create_leaf(sample_graph):
    def request(leaf, *args, **kwargs):
        node = LeafNode()
        node.leaf_id = leaf.leaf_id
        sample_graph.create(node)
    return request


# TODO: Replace with endpoint request
@fixture
def get_leaf(sample_graph):
    def request(leaf_id, ensure=False, *args, **kwargs):
        node = LeafNode.match(sample_graph, leaf_id).limit(1)
        if ensure:
            assert len(node) > 0
        return node.first()
    return request


@fixture
def get_nearest_leaf(make_request):
    def request(experiment_id, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{experiment_id}/nearest-leaf-node', 'GET', *args, **kwargs)
    return request


settings.register_profile('e2e', deadline=None)
settings.load_profile('e2e')
