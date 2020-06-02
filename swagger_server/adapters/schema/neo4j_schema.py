from py2neo import Graph, Schema

from swagger_server.adapters.ogm.neo4j import SampleNode


def apply_schema(graph: Graph):
    schema = Schema(graph)

    if SampleNode.__primarykey__ not in schema.get_uniqueness_constraints(SampleNode.__primarylabel__):
        schema.create_uniqueness_constraint(SampleNode.__primarylabel__, SampleNode.__primarykey__)
