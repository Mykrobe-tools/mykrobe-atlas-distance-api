from random import sample, random, randrange

from neomodel import db, config

from swagger_server.orm.DistanceORM import SampleNode

N_NODES = 5


def get_num_neighbors():
    return randrange(1, 4)  # 1 to 3 neighbors


config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
config.ENCRYPTED_CONNECTION = False

nodes = SampleNode.create(*[{'name': 's%d' % i} for i in range(N_NODES)])

for i in range(N_NODES):
    rest = nodes[:i] + nodes[i+1:]
    neighbors = sample(rest, get_num_neighbors())
    node = nodes[i]

    for n2 in rest:
        query = f'MATCH (n1:SampleNode),(n2:SampleNode) WHERE n1.name="{node.name}" AND n2.name="{n2.name}" ' \
                f'CREATE (n1)-[:NEIGHBOR {{dist: {random()}}}]->(n2) CREATE (n1)-[:PARENT]->(n2) ' \
                f'RETURN n1,n2 '
        db.cypher_query(query)
