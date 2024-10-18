import sqlite3
import pandas as pd
# Fetch table data from the database
def get_table_data(DB_PATH, table_name):
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM {table_name};"
    data = pd.read_sql(query, conn)
    conn.close()

    return data

# Execute a custom SQL query
def execute_sql_query(DB_PATH, query):
    conn = sqlite3.connect(DB_PATH)
    result = pd.read_sql(query, conn)
    conn.close()
        
    return result
