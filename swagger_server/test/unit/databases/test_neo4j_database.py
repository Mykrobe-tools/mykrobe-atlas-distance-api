from hypothesis import given
from py2neo.ogm import GraphObject, Property

from swagger_server.test.strategies import safe_strings


class SomeObject(GraphObject):
    name = Property()


@given(name=safe_strings())
def test_creating_node_from_graph_object(db, name):
    try:
        obj = SomeObject()
        obj.name = name

        db.create(obj)

        matched_nodes = db.node_matcher.match(name=name)
        assert len(matched_nodes) == 1
    finally:
        db.truncate()
