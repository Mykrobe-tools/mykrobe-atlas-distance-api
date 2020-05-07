from neo4j import GraphDatabase
from neobolt.exceptions import ClientError


def unique_sample_names(tx):
    tx.run('CREATE CONSTRAINT ON (a:SampleNode) ASSERT a.name IS UNIQUE')


def unique_lineage_names(tx):
    tx.run('CREATE CONSTRAINT ON (a:LineageNode) ASSERT a.name IS UNIQUE')


def migrate(driver):
    with driver.session() as s:
        try:
            s.write_transaction(unique_sample_names)
        except ClientError as e:
            if 'already exist' not in str(e):
                raise
            pass
        try:
            s.write_transaction(unique_lineage_names)
        except ClientError as e:
            if 'already exist' not in str(e):
                raise
            pass


if __name__ == '__main__':
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, encrypted=False)
    migrate(driver)
