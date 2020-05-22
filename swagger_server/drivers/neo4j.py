from typing import Union

from py2neo import Graph, Subgraph, ClientError, DatabaseError
from py2neo.ogm import GraphObject

from swagger_server.drivers.base import BaseDriver
from swagger_server.drivers.exceptions import SchemaExistedError, UniqueConstraintViolationError, \
    SchemaDoesNotExistError

GraphState = Union[Subgraph, GraphObject]


class Neo4jDriver(BaseDriver):
    uri = 'bolt://localhost:7687'
    encrypted = False

    @classmethod
    def make_instance(cls) -> Union['Neo4jDriver']:
        return Neo4jDriver()

    def __init__(self):
        self.graph = Graph(self.uri, secure=self.encrypted)

    def create_new(self, changes: GraphState):
        # Enforce creating new for GraphObject instances
        if isinstance(changes, GraphObject):
            changes = changes.__ogm__.node

        tx = self.graph.begin()
        try:
            tx.create(changes)
        except ClientError as e:
            if 'ConstraintValidationFailed' in e.code:
                raise UniqueConstraintViolationError
        else:
            tx.commit()

    def apply_changes(self, changes: GraphState):
        self.graph.push(changes)

    def verify_changes(self, changes: GraphState) -> bool:
        return self.graph.exists(changes)

    def execute(self, query: str):
        return self.graph.evaluate(query)

    def modify_schema(self, query: str):
        try:
            self.execute(query)
        except ClientError as e:
            if 'EquivalentSchemaRuleAlreadyExists' in e.code:
                raise SchemaExistedError
        except DatabaseError as e:
            if 'No such constraint' in e.message:
                raise SchemaDoesNotExistError

    def clear_db(self):
        self.graph.delete_all()
