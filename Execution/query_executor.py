import time

from config.enums import Schema
from database.pool import db_pool


class SchemaViolationError(Exception):
    """Raised when query attempts to modify data."""
    pass


class QueryExecutor:
    """
    Safe query executor with read-only enforcement.
    """

    FORBIDDEN_KEYWORDS = {
        "CREATE", "DROP", "ALTER", "TRUNCATE",
        "INSERT", "UPDATE", "DELETE",
    }

    def _validate_query(self, query):
        """Check if query contains forbidden keywords."""
        query_upper = query.upper()
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in query_upper:
                raise SchemaViolationError(f"Forbidden keyword: {keyword}")

    def execute_query(self, query, schema):
        """
        Execute a SQL query on the specified schema.

        Returns:
            Dict with rows, columns, row_count, execution_time, error
        """
        self._validate_query(query)

        result = {
            "rows": [],
            "columns": [],
            "row_count": 0,
            "execution_time": 0,
            "error": None,
        }

        start_time = time.time()

        try:
            with db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SET search_path TO {schema.value}")
                    cursor.execute(query)

                    if cursor.description:
                        result["columns"] = [desc[0] for desc in cursor.description]
                        raw_rows = cursor.fetchall()
                        result["rows"] = [
                            dict(zip(result["columns"], row)) for row in raw_rows
                        ]
                        result["row_count"] = len(result["rows"])

                    result["execution_time"] = time.time() - start_time
                    print(f"Query executed: {result['row_count']} rows in {result['execution_time']:.3f}s")

        except Exception as e:
            result["error"] = str(e)
            result["execution_time"] = time.time() - start_time

        return result


# Global instance
query_executor = QueryExecutor()