from contextlib import contextmanager

from py2neo import Graph

from swagger_server.adapters.schema import neo4j_schema


@contextmanager
def managed_db():
    graph = Graph()
    neo4j_schema.apply_schema(graph)

    yield Graph()

    graph.delete_all()
