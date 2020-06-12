from concurrent.futures.thread import ThreadPoolExecutor

from swagger_server.repositories import Neo4jRepository


def test_database_connections_are_shared():
    a = Neo4jRepository()
    b = Neo4jRepository()
    assert a.driver is b.driver

    with ThreadPoolExecutor() as exc:
        future = exc.submit(lambda: Neo4jRepository())
    b = future.result()
    assert a.driver is b.driver
