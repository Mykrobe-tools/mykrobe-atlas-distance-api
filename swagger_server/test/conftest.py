from pytest import fixture

from swagger_server.test.fixtures import managed_db


@fixture
def db():
    with managed_db() as db:
        yield db
