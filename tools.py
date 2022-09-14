from typing import Tuple

import pandas as pd
from cassandra.cluster import Cluster, Session


class CassandraHandler():
    """Handle Apache Cassandra Operations."""

    @staticmethod
    def create_cluster_and_session() -> Tuple[Cluster, Session]:
        """Returns Cassandra's cluster and connection.

        Local machine instance on 127.0.0.1."""

        cluster = Cluster()
        session = cluster.connect()

        return cluster, session

    @staticmethod
    def close_cluster_and_session(cluster: Cluster, session: Session):
        """Close Cassandra's cluster and connection."""

        session.shutdown()
        cluster.shutdown()

    @staticmethod
    def execute(session: Session, query: str):
        """Execute query statement."""

        try:
            session.execute(query)
        except Exception as e:
            print(e)

    @staticmethod
    def drop_table(session: Session, table_name: str):
        """Drop table if exists."""

        try:
            session.execute(f"DROP TABLE IF EXISTS {table_name}")
        except Exception as e:
            print(e)

    @staticmethod
    def get_query_results(session: Session, query: str):
        """Get query results and length."""

        try:
            res = list(session.execute(query))
            return pd.DataFrame(res)

        except Exception as e:
            print(e)

    @staticmethod
    def create_keyspace(session: Session):
        """Create Cassandra's keyspace."""

        try:
            session.execute("""
                CREATE KEYSPACE IF NOT EXISTS udacity
                WITH REPLICATION = {
                    'class': 'SimpleStrategy',
                    'replication_factor': 1
                }
            """)
        except Exception as e:
            print(e)

    @staticmethod
    def set_keyspace(session: Session, name: str):
        """Set Cassandra's keyspace."""

        try:
            session.set_keyspace(name)

        except Exception as e:
            print(e)

    @staticmethod
    def insert_into(session: Session, insert: str, values: Tuple):
        """Insert."""

        try:
            session.execute(insert, values)

        except Exception as e:
            print(e)
