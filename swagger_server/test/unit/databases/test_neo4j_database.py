from hypothesis import given
from hypothesis.strategies import text
from py2neo import Schema
from py2neo.ogm import GraphObject, Property
from pytest import raises, fixture

from swagger_server.databases.exceptions import UniqueConstraintViolated


@fixture
def db(db):
    label = SomeObject.__name__
    property_key = 'name'
    schema = Schema(db.graph)
    schema.create_uniqueness_constraint(label, property_key)

    try:
        yield db
    finally:
        schema.drop_uniqueness_constraint(label, property_key)


class SomeObject(GraphObject):
    name = Property()


@given(name=text())
def test_creating_node_from_graph_object(db, name):
    try:
        obj = SomeObject()
        obj.name = name

        db.create(obj)

        matched_nodes = db.node_matcher.match(name=name)
        assert len(matched_nodes) == 1
    finally:
        db.truncate()


def test_creating_duplicated_node(db):
    name = 'some name'
    obj = SomeObject()
    obj.name = name
    another = SomeObject()
    another.name = name

    db.create(obj)
    with raises(UniqueConstraintViolated):
        db.create(another)
