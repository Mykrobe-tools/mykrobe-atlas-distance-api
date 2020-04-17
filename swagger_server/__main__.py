#!/usr/bin/env python3
import os

import connexion
from neomodel import config, db

from swagger_server import encoder
from swagger_server.orm.DistanceORM import SampleNode


@db.transaction
def create_dummy_data():
    samples = []
    for name in ['s1', 's2', 's3']:
        try:
            s = SampleNode.nodes.get(name=name)
        except SampleNode.DoesNotExist:
            s = SampleNode(name=name).save()
        samples.append(s)
    samples[0].neighbors.connect(samples[1], {'dist': 5})
    samples[0].neighbors.connect(samples[2], {'dist': 10})


def main():
    config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
    config.ENCRYPTED_CONNECTION = False

    create_dummy_data()

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Distance API'}, pythonic_params=True)
    app.run(port=8080, debug=os.environ.get('DEBUG'))


if __name__ == '__main__':
    main()
