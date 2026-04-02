import os
import sys
import psycopg2

# Add root directory to sys.path to import config modules
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from config.settings import DB_CONFIG

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ecommerce.expected_results (
    problem_id VARCHAR(50) PRIMARY KEY,
    result_hash VARCHAR(255) NOT NULL,
    result_rows JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a function to auto-update the updated_at timestamp
CREATE OR REPLACE FUNCTION ecommerce.update_expected_results_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger using the function
DROP TRIGGER IF EXISTS trigger_expected_results_updated_at ON ecommerce.expected_results;
CREATE TRIGGER trigger_expected_results_updated_at
    BEFORE UPDATE ON ecommerce.expected_results
    FOR EACH ROW
    EXECUTE FUNCTION ecommerce.update_expected_results_updated_at();
"""

def create_table():
    print(f"Connecting to database '{DB_CONFIG.get('database')}' at {DB_CONFIG.get('host')}...")
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        
        with conn.cursor() as cur:
            print("Creating expected_results table...")
            cur.execute(CREATE_TABLE_SQL)
            print("Successfully created the expected_results table.")
            
    except Exception as e:
        print(f"Error creating table: {e}")
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    create_table()
