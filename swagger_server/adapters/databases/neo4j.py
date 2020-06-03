from py2neo import Graph
from py2neo.ogm import GraphObject

from swagger_server.adapters.databases.base import IDatabase


class Neo4jDatabase(IDatabase):

    def __init__(self, uri=None, **settings):
        self.graph = Graph(uri, **settings)

    def create(self, obj: GraphObject):
        # The `py2neo.Graph.create` method on error will throw two exceptions, in the order below:
        #
        # 1. A ClientError exception which contain useful description of the error
        # 2. A GraphTransactionError which does not contain useful info
        #
        # The problem is that the latter is raised without traceback to the former, therefore we cannot
        # catch the former error (which is useful) in code, we can only see it in the log.
        #
        # Further debugging revealed that the latter error is raised because the transaction attempt to rollback
        # twice, so this is probably a bug on py2neo side.
        #
        # To circumvent said problem, we manually operate the transaction:

        tx = self.graph.begin()
        try:
            tx.create(obj)
        except Exception:
            raise
        else:
            tx.commit()

    def truncate(self):
        self.graph.delete_all()
