from neo4j import Transaction

from swagger_server.models import Sample


def create_sample(tx: Transaction, sample: Sample):
    create_sample_q = 'CREATE (s:SampleNode {name: $name}) '
    create_neighbours = ''
    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            create_neighbours += f'CREATE (s)-[:NEIGHBOUR {{dist: {neighbour.distance}}}]->(:SampleNode {{name: "{neighbour.experiment_id}"}}) '

    query = create_sample_q + create_neighbours
    tx.run(query, name=sample.experiment_id)


def create_or_update_sample(tx: Transaction, sample: Sample):
    create_or_update_sample_q = 'MERGE (s:SampleNode {name: $name}) '
    create_or_update_neighbours = ''
    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            create_or_update_neighbours += f'MERGE (s)-[:NEIGHBOUR {{dist: {neighbour.distance}}}]->(:SampleNode {{name: "{neighbour.experiment_id}"}}) '

    query = create_or_update_sample_q + create_or_update_neighbours
    tx.run(query, name=sample.experiment_id)
