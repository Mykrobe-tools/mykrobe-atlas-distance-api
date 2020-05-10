from swagger_server.helpers import db


def cleanup_each_example(func):
    def wrapped(test_case_instance, *args, **kwargs):
        try:
            return func(test_case_instance, *args, **kwargs)
        finally:
            db.Neo4jDatabase.get().query('MATCH (n) DETACH DELETE n', write=True)

    return wrapped