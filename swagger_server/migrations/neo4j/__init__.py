from swagger_server.migrations.neo4j import unique_sample_name

NEO4J_MIGRATIONS = [
    (unique_sample_name.FORWARD, unique_sample_name.BACKWARD),
]