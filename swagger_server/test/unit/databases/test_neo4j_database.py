from hypothesis import given
from py2neo import Schema, ClientError
from py2neo.ogm import GraphObject, Property
from pytest import fixture, raises

from swagger_server.test.strategies import safe_strings


PROP_NAME = 'some_prop'


class SomeObject(GraphObject):
    some_prop = Property()


@given(prop=safe_strings())
def test_creating_graph_objects(db, prop):
    try:
        obj = SomeObject()
        obj.some_prop = prop

        db.create_or_merge(obj)

        matched_nodes = db.graph.nodes.match(SomeObject.__primarylabel__, **{PROP_NAME: prop})
        assert len(matched_nodes) == 1
    finally:
        db.truncate()


@fixture
def schematised_db(db):
    schema = Schema(db.graph)
    schema.create_uniqueness_constraint(SomeObject.__primarylabel__, PROP_NAME)

    try:
        yield db
    finally:
        schema.drop_uniqueness_constraint(SomeObject.__primarylabel__, PROP_NAME)


class TestUniqueConstraint:
    def test_creating_duplicated_objects_without_primary_key_raises_error(self, schematised_db):
        value = 'some value'

        obj = SomeObject()
        obj.some_prop = value
        other = SomeObject()
        other.some_prop = value

        schematised_db.create_or_merge(obj)
        with raises(ClientError):
            schematised_db.create_or_merge(other)

        matched_nodes = schematised_db.graph.nodes.match(SomeObject.__primarylabel__, **{PROP_NAME: value})
        assert len(matched_nodes) == 1

    def test_creating_duplicated_objects_with_primary_key_merge_objects_instead(self, schematised_db):
        SomeObject.__primarykey__ = PROP_NAME
        value = 'some value'

        obj = SomeObject()
        obj.some_prop = value
        other = SomeObject()
        other.some_prop = value

        schematised_db.create_or_merge(obj)
        schematised_db.create_or_merge(other)

        matched_nodes = schematised_db.graph.nodes.match(SomeObject.__primarylabel__, **{PROP_NAME: value})
        assert len(matched_nodes) == 1
