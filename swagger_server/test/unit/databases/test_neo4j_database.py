from hypothesis import given
from py2neo import Schema, ClientError
from py2neo.ogm import GraphObject, Property
from pytest import fixture, raises

from swagger_server.test.strategies import safe_strings


@fixture
def db(db):
    schema = Schema(db.graph)
    property_key = 'name'
    schema.create_uniqueness_constraint(SomeObject.__primarylabel__, property_key)

    try:
        yield db
    finally:
        schema.drop_uniqueness_constraint(SomeObject.__primarylabel__, property_key)


class SomeObject(GraphObject):
    name = Property()


@given(name=safe_strings())
def test_creating_node_from_graph_object(db, name):
    try:
        obj = SomeObject()
        obj.name = name

        db.create(obj)

        matched_nodes = db.graph.nodes.match(SomeObject.__primarylabel__, name=name)
        assert len(matched_nodes) == 1
    finally:
        db.truncate()


def test_creating_duplicated_node(db):
    name = 'some name'
    obj = SomeObject()
    obj.name = name
    other = SomeObject()
    other.name = name

    db.create(obj)
    with raises(ClientError):
        db.create(other)

    matched_nodes = db.graph.nodes.match(SomeObject.__primarylabel__, name=name)
    assert len(matched_nodes) == 1


def test_creating_duplicated_node_with_primary_key(db):
    SomeObject.__primarykey__ = 'name'

    name = 'some name'
    obj = SomeObject()
    obj.name = name
    other = SomeObject()
    other.name = name

    db.create(obj)
    db.create(other)

    matched_nodes = db.graph.nodes.match(SomeObject.__primarylabel__, name=name)
    assert len(matched_nodes) == 1
