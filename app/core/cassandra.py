from cassandra.cluster import Cluster

CASSANDRA_HOST = "127.0.0.1"
CASSANDRA_PORT = 9042
KEYSPACE = "financial_dwh"

_session = None


def get_session():
    global _session

    if _session is None:
        cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
        _session = cluster.connect(KEYSPACE)

    return _session
