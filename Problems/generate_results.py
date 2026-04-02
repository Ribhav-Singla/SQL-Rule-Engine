import json
import sys
import os

# Add root directory to sys.path to import database and config modules
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

try:
    import sqlglot
except ImportError:
    print("sqlglot is not installed. Please run 'pip install sqlglot'")
    sys.exit(1)

from database.pool import db_pool
from normalization.result import normalize_result
from hasher.fingerprint import generate_sha256_hash
from normalization.query import normalize_sql

import psycopg2
from config.settings import DB_CONFIG

def main():
    problems_path = os.path.join(current_dir, 'problems.json')
    output_path = os.path.join(current_dir, 'expected_results.json')
    
    if not os.path.exists(problems_path):
        print(f"Error: {problems_path} does not exist.")
        sys.exit(1)
        
    with open(problems_path, 'r') as f:
        problems = json.load(f)
        
    results = []
    
    try:
        # Obtain connection from the existing pool
        with db_pool.get_connection() as conn:
            for prob in problems:
                problem_id = prob['problem_id']
                original_query = prob.get('query', '')
                schema = prob.get('schema', '')
                
                if not original_query:
                    print(f"Skipping {problem_id}: No query provided.")
                    continue
                
                print(f"Processing {problem_id}...")
                
                # Step 1: Parse and normalize the query
                try:
                    normalize_sql_query = normalize_sql(original_query)
                    ast = normalize_sql_query["ast"]
                    normalized_query = normalize_sql_query["normalized_sql"]
                except Exception as e:
                    print(f"  [Warning] Normalization failed for {problem_id}: {e}")
                    normalized_query = original_query
                
                # Step 2: Run the query against DB
                try:
                    with conn.cursor() as cur:
                        if schema:
                            # Ensuring we execute within the correct schema context
                            cur.execute(f"SET search_path TO {schema}")
                            
                        cur.execute(normalized_query)
                        rows = cur.fetchall()
                        columns = [desc[0] for desc in cur.description]
                        
                        # Step 3: Convert fetched tuples to dictionaries
                        dict_rows = [dict(zip(columns, row)) for row in rows]
                        
                        # Step 4: Normalize result rows to a deterministic JSON string
                        # Using the existing normalize_result from normalization.result
                        result_json_str = normalize_result(dict_rows)
                        
                        # Step 5: Hash the normalized JSON string
                        # Using the existing generate_sha256_hash from hasher.fingerprint
                        result_hash = generate_sha256_hash(result_json_str)
                        
                        results.append({
                            "problem_id": problem_id,
                            "result_hash": result_hash,
                            "result_rows": result_json_str
                        })
                        print(f"  [Success] Scanned {len(rows)} rows. Hash: {result_hash[:10]}...")
                        
                except Exception as e:
                    print(f"  [Error] Failed executing query for {problem_id}: {e}")
                    # Need to rollback the failed transaction block to continue using connection
                    conn.rollback()

    except Exception as e:
        print(f"Fatal error interacting with database: {e}")
        sys.exit(1)
        
    # Final Step: Store in the output JSON file
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"\nProcessing complete. Results saved to {output_path}")

    # NEW STEP: Store results in the expected_results table
    print("Saving results to ecommerce.expected_results table...")
    try:
        write_conn = psycopg2.connect(**DB_CONFIG)
        write_conn.autocommit = True
        with write_conn.cursor() as write_cur:
            for r in results:
                insert_sql = """
                    INSERT INTO ecommerce.expected_results (problem_id, result_hash, result_rows)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (problem_id) DO UPDATE SET
                        result_hash = EXCLUDED.result_hash,
                        result_rows = EXCLUDED.result_rows;
                """
                write_cur.execute(insert_sql, (r['problem_id'], r['result_hash'], r['result_rows']))
        print("Successfully saved all results to the database table.")
    except Exception as e:
        print(f"Failed to save results to database: {e}")
    finally:
        if 'write_conn' in locals() and write_conn:
            write_conn.close()

if __name__ == "__main__":
    main()
