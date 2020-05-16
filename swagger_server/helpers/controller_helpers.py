from swagger_server.helpers import db


def with_db(func):
    def wrapped(*args, **kwargs):
        with db.Neo4jDatabase().get():
            return func(*args, **kwargs)
    return wrapped
