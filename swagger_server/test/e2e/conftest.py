import logging

import connexion
from flask import g
from hypothesis import settings
from py2neo import Graph
from pytest import fixture

from swagger_server.encoder import JSONEncoder


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
    def request(path, method, json=None):
        return client.open(path, method=method, json=json)
    return request


API_ROOT = '/api/v1'


@fixture
def create_sample(make_request):
    def request(sample):
        return make_request(f'{API_ROOT}/samples', 'POST', sample)
    return request


@fixture
def get_sample(make_request):
    def request(sample):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}', 'GET')
    return request


@fixture
def delete_sample(make_request):
    def request(sample):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}', 'DELETE')
    return request


@fixture
def get_neighbours(make_request):
    def request(sample):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}/nearest-neighbours', 'DELETE')
    return request


@fixture
def update_neighbours(make_request):
    def request(sample, neighbours):
        return make_request(f'{API_ROOT}/samples/{sample.experiment_id}/nearest-neighbours', 'PUT', neighbours)
    return request


settings.register_profile('e2e', deadline=None)
settings.load_profile('e2e')
