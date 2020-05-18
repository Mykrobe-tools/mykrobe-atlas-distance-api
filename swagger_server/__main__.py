#!/usr/bin/env python3
import os

import connexion

from swagger_server import encoder
from swagger_server.helpers import db


def main():
    db.URI = "bolt://localhost:7687"
    db.ENCRYPTED = False

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Distance API'})

    with db.Neo4jDatabase.get():
        app.run(port=8080, debug=os.environ.get('DEBUG'))


if __name__ == '__main__':
    main()
