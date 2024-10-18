import sqlite3

def setup_test_schema(conn):
    # Create a test table schema
    conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, age INTEGER);')
    # Add more tables or columns if necessary

def validate_sql(query):
    # Create an in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    
    # Set up the test schema
    setup_test_schema(conn)
    
    try:
        # Try executing the SQL statement
        conn.execute(query)
        return True
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
        return False
    finally:
        conn.close()

# Example usage
sql_query = "SELECT * FROM users WHERE salary > 30;"
if validate_sql(sql_query):
    print("Valid SQL Query")
else:
    print("Invalid SQL Query")
