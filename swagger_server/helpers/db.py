from threading import local

from neo4j import GraphDatabase


URI = ""
ENCRYPTED = True


class Database(local):
    db = None

    def __init__(self):
        self.driver = GraphDatabase.driver(URI, encrypted=ENCRYPTED)

    def query(self, q):
        with self.driver.session() as s:
            result = s.write_transaction(lambda tx: tx.run(q))

        return result

    @classmethod
    def get(cls):
        if not cls.db:
            cls.db = Database()
        return cls.db

    def close(self):
        self.driver.close()
