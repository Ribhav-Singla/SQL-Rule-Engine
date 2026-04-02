import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

from config.settings import DB_CONFIG


class DatabasePool:
    """
    PostgreSQL connection pool with read-only access.
    Lazily initialized — won't connect until first use.
    """

    def __init__(self):
        self._pool = None

    def initialize(self):
        """Initialize the connection pool from config settings."""
        self._pool = pool.ThreadedConnectionPool(
            minconn=5,
            maxconn=20,
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        print("Database pool initialized")

    def _ensure_pool(self):
        """Auto-initialize if not already done."""
        if self._pool is None:
            self.initialize()

    @contextmanager
    def get_connection(self):
        """Get a read-only connection from the pool."""
        self._ensure_pool()
        conn = self._pool.getconn()
        try:
            conn.set_session(readonly=True)
            yield conn
        finally:
            conn.rollback()
            self._pool.putconn(conn)

    def close_all(self):
        """Close all connections."""
        if self._pool:
            self._pool.closeall()


# Global instance (lazy — no connection at import time)
db_pool = DatabasePool()