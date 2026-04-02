import os
import sys

# Add root directory to sys.path to import config modules
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

try:
    import psycopg2
except ImportError:
    print("psycopg2 is not installed. Please run 'pip install psycopg2-binary'")
    sys.exit(1)

from config.settings import DB_CONFIG

def seed_database():
    seed_file = os.path.join(current_dir, 'seed.sql')
    if not os.path.exists(seed_file):
        print(f"Error: {seed_file} does not exist.")
        sys.exit(1)
        
    print(f"Reading seed file: {seed_file}")
    with open(seed_file, 'r', encoding='utf-8') as f:
        sql = f.read()
        
    print(f"Connecting to database {DB_CONFIG.get('database')} at {DB_CONFIG.get('host')}...")
    conn = None
    try:
        # Connect to the DB using settings
        conn = psycopg2.connect(**DB_CONFIG)
        # Enable autocommit
        conn.autocommit = True
        
        with conn.cursor() as cur:
            print("Executing SQL statements...")
            cur.execute(sql)
            print("Successfully seeded the database.")
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    seed_database()
