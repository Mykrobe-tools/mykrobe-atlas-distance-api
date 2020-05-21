from neo4j import Transaction

from swagger_server.models import Sample


def create_sample(tx: Transaction, name: str) -> Sample:
    result = tx.run('CREATE (s:SampleNode {name: $name}) RETURN s', name=name).single().value()
    return Sample(result['name'])
