from swagger_server.drivers.neo4j import Neo4jDriver


def cleanup_each_example(func):
    def wrapped(test_case_instance, *args, **kwargs):
        try:
            return func(test_case_instance, *args, **kwargs)
        finally:
            Neo4jDriver.get().delete_all()

    return wrapped
