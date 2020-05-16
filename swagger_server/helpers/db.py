from threading import local

from neo4j import GraphDatabase


URI = ""
ENCRYPTED = True


class Neo4jDatabase(local):
    db = None

    def __init__(self):
        self.driver = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self):
        self.driver = GraphDatabase.driver(URI, encrypted=ENCRYPTED)

    def close(self):
        self.driver.close()

    def query(self, q, write=False):
        """
        Execute a Cypher query in a managed transaction

        Keyword arguments:
            q -- The query to be executed.
            write -- Whether this is a query that will modify data. False by default.
        """
        if not self.driver:
            raise RuntimeError("neo4j driver not created. Did you use the helper in a context manager?")

        with self.driver.session() as s:
            if write:
                result = s.write_transaction(lambda tx: tx.run(q))
            else:
                result = s.read_transaction(lambda tx: tx.run(q))

        return result

    @classmethod
    def get(cls):
        if not cls.db:
            cls.db = Neo4jDatabase()
        return cls.db
