from neo4j import Transaction

from swagger_server.models import Sample


def merge_sample(tx: Transaction, sample: Sample):
    create_or_update_sample = 'MERGE (s:SampleNode {name: $name}) '
    create_or_update_neighbours = ''
    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            create_or_update_neighbours += f'MERGE (s)-[:NEIGHBOUR {{dist: {neighbour.distance}}}]->(:SampleNode {{name: "{neighbour.experiment_id}"}}) '

    query = create_or_update_sample + create_or_update_neighbours
    tx.run(query, name=sample.experiment_id)
