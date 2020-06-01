from contextlib import contextmanager

from py2neo import Graph


@contextmanager
def managed_db():
    graph = Graph()
    yield Graph()
    graph.delete_all()
