from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, encrypted=False)


def unique_sample_names(tx):
    tx.run('CREATE CONSTRAINT ON (a:SampleNode) ASSERT a.name IS UNIQUE')


def unique_lineage_names(tx):
    tx.run('CREATE CONSTRAINT ON (a:LineageNode) ASSERT a.name IS UNIQUE')


def main():
    with driver.session() as s:
        s.write_transaction(unique_sample_names)
        s.write_transaction(unique_lineage_names)


if __name__ == '__main__':
    main()
