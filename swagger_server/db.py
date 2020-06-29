from py2neo import Graph

db = None


def get_db():
    global db
    if not db:
        db = Graph()
    return db
