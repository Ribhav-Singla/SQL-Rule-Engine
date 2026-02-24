import psycopg2
from psycopg2 import pool
from contextlib import contextmanager


class DatabasePool:
    """
    Simple PostgreSQL connection pool with read-only access
    """
    def __init__(self):
        self.pool = None

    def initialize(self, host="localhost", port=5432, database="sqlruleengine",
                   user="readonly_user", password="readonly_pass"):
        """
        Initialize the connection pool
        """
        self.pool = pool.ThreadedConnectionPool(
            minconn=5,
            maxconn=20,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Database pool initialized")

    @contextmanager
    def get_connection(self):
        """
        Get a connection from the pool
        """
        conn = self.pool.getconn()
        try:
            conn.set_session(readonly=True)
            yield conn
        finally:
            conn.rollback()
            self.pool.putconn(conn)

    def close_all(self):
        """
        Close all connections
        """
        if self.pool:
            self.pool.closeall()


# Global instance
_dbPool = DatabasePool()