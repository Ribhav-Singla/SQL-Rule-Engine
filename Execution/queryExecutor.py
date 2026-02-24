import psycopg2
import time
from utils import Schema
from Database.poolDb import DatabasePool

db_pool = DatabasePool()
db_pool.initialize(
    host="localhost",
    port=5432,
    database="sqlruleengine",
    user="postgres",
    password="postgres"
)


class SchemaViolationError(Exception):
    """Raised when query attempts to modify data"""
    pass


class QueryExecutor:
    """
    Simple query executor with read-only enforcement
    """
    
    FORBIDDEN_KEYWORDS = {
        'CREATE', 'DROP', 'ALTER', 'TRUNCATE',
        'INSERT', 'UPDATE', 'DELETE'
    }

    def _validate_query(self, query):
        """
        Check if query contains forbidden keywords
        """
        query_upper = query.upper()
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword in query_upper:
                raise SchemaViolationError(f"Forbidden keyword: {keyword}")

    def execute_query(self, query, schema):
        """
        Execute a SQL query on the specified schema
        
        Returns:
            Dict with rows, columns, row_count, execution_time, error
        """
        self._validate_query(query)
        
        result = {
            "rows": [],
            "columns": [],
            "row_count": 0,
            "execution_time": 0,
            "error": None
        }
        
        start_time = time.time()
        
        try:
            with db_pool.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Set schema and execute query
                    cursor.execute(f"SET search_path TO {schema.value}")
                    cursor.execute(query)
                    
                    # Get results
                    if cursor.description:
                        result["columns"] = [desc[0] for desc in cursor.description]
                        result["rows"] = cursor.fetchall()
                        result["row_count"] = len(result["rows"])
                    
                    result["execution_time"] = time.time() - start_time
                    print(f"Query executed: {result['row_count']} rows in {result['execution_time']:.3f}s")
                    
        except Exception as e:
            result["error"] = str(e)
            result["execution_time"] = time.time() - start_time
        
        return result


# Global instance
_queryExecutor = QueryExecutor()