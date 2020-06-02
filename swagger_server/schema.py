from py2neo import Schema

from swagger_server.adapters.object_mappers.neo4j import SampleNode, LeafNode
from swagger_server.adapters.databases.neo4j import Neo4jDatabase


def apply(db: Neo4jDatabase):
    schema = Schema(db.graph)
    schema.create_uniqueness_constraint(SampleNode.__primarylabel__, SampleNode.__primarykey__)
    schema.create_uniqueness_constraint(LeafNode.__primarylabel__, LeafNode.__primarykey__)


def unapply(db: Neo4jDatabase):
    schema = Schema(db.graph)
    schema.drop_uniqueness_constraint(SampleNode.__primarylabel__, SampleNode.__primarykey__)
    schema.drop_uniqueness_constraint(LeafNode.__primarylabel__, LeafNode.__primarykey__)
