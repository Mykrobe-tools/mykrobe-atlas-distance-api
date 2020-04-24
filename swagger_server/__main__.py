#!/usr/bin/env python3
import os

import connexion
from neomodel import config

from swagger_server import encoder


def main():
    config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
    config.ENCRYPTED_CONNECTION = False

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Distance API'})
    app.run(port=8080, debug=os.environ.get('DEBUG'))


if __name__ == '__main__':
    main()
