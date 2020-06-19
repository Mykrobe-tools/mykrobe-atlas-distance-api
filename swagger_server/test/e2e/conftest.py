import logging

import connexion
from flask import g
from hypothesis import settings
from py2neo import Graph
from pytest import fixture

from swagger_server.encoder import JSONEncoder
from swagger_server.ogm import LeafNode


@fixture
def sample_graph():
    repo = Graph()
    yield repo
    repo.delete_all()


@fixture
def app(sample_graph):
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../../openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('openapi.yaml')

    with app.app.app_context():
        g.sample_graph = sample_graph
        yield app.app


@fixture
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
    def request(sample, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}', 'GET', *args, **kwargs)
    return request


@fixture
def delete_sample(make_request):
    def request(sample):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}', 'DELETE')
    return request


@fixture
def get_neighbours(make_request):
    def request(sample, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}/nearest-neighbours', 'DELETE', *args, **kwargs)
    return request


@fixture
def update_neighbours(make_request):
    def request(sample, neighbours, *args, **kwargs):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}/nearest-neighbours', 'PUT', neighbours, *args, **kwargs)
    return request


# TODO: Replace with endpoint request
@fixture
def create_leaf(sample_graph):
    def request(leaf, *args, **kwargs):
        node = LeafNode()
        node.leaf_id = leaf.leaf_id
        sample_graph.create(node)
    return request


settings.register_profile('e2e', deadline=None)
settings.load_profile('e2e')
