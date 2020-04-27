from neomodel import config, db

config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
config.ENCRYPTED_CONNECTION = False


def main():
    db.cypher_query('CREATE CONSTRAINT ON (a:SampleNode) ASSERT a.name IS UNIQUE')
    db.cypher_query('CREATE CONSTRAINT ON (a:LineageNode) ASSERT a.name IS UNIQUE')


if __name__ == '__main__':
    main()
