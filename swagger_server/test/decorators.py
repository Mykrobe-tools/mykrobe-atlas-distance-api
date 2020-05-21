from swagger_server.drivers.neo4j import Neo4jDriver


def cleanup_each_example(func):

    def wrapped(test_case_instance, *args, **kwargs):
        try:
            return func(test_case_instance, *args, **kwargs)
        finally:
            with Neo4jDriver.get() as driver:
                with driver.driver.session() as s:
                    s.write_transaction(lambda tx: tx.run('MATCH (n) DETACH DELETE n'))

    return wrapped
