import sqlite3
import sqlparse
import streamlit as st
from model import get_sql  # Import from the new module
from database import get_table_data, execute_sql_query

DB_PATH = "chinook.db"

# Define available tables
TABLES = ["employees", "customers", "tracks", "albums", "artists", "genres"]

# Define the clean_sql_output function
def clean_sql_output(sql_query, table_name):
    # Remove unwanted tokens like '<pad>' and '</s>'
    cleaned_query = sql_query.replace('<pad>', '').replace('</s>', '')

    # Replace the word "table" with "employees"
    cleaned_query = cleaned_query.replace('table', table_name)

    # Remove any extra leading/trailing whitespace
    cleaned_query = cleaned_query.strip()

    return cleaned_query

def validate_sql(query, db_file=DB_PATH):
    # Connect to the SQLite database file
    conn = sqlite3.connect(db_file)
    
    try:
        # Try executing the SQL statement
        conn.execute(query)
        return True
    except sqlite3.Error as e:
        return (f"SQL Error: {e}")
    finally:
        conn.close()

def format_sql_query(sql_query):
    # Format SQL query with sqlparse and convert keywords to uppercase
    formatted_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')

    # Replace newlines with spaces to make it one line
    formatted_query = ' '.join(formatted_query.split())
    
    return formatted_query

# Streamlit app interface
def main():
    st.title("Text to SQL Converter")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Home", "Playground"])

    if selected_page == "Home":
        show_home()
    elif selected_page == "Playground":
        show_playground()


def show_home():
    # Choose a table (Dropdown or Radio buttons)
    selected_table = st.radio("Select a table to query from:", TABLES)

    # Input natural language query
    user_query = st.text_area("Enter your question in natural language:", height=150)

    if st.button("Generate SQL"):
        if user_query:
            # Generate SQL query
            sql_query = get_sql(user_query)
            cleaned_query = clean_sql_output(sql_query, selected_table)

            # Format the SQL query
            formatted_query = format_sql_query(cleaned_query)

            # Display the generated SQL
            st.subheader("Generated SQL Query:")
            st.code(formatted_query, language='sql')

            # Validate the SQL query
            validation_result = validate_sql(formatted_query)
            if validation_result == True:
                st.success("SQL query is valid and executable.")
            else:
                st.error(validation_result)

# Show playground functionality
def show_playground():
    st.header("SQL Playground")

    # Select a table to view
    selected_table = st.radio("Select a table to view:", TABLES)

    if selected_table:
        st.text(f"Table Selected: {selected_table}")
        
        # Show the selected table's data (initially) without index
        table_data = get_table_data(DB_PATH, selected_table)
        st.write(table_data)

        # SQL input for custom queries (now placed below the table)
        st.subheader("Input SQL Query")
        custom_query = st.text_area("Write your SQL query here:", value=f"SELECT * FROM {selected_table};", height=150)

        # Execute the query and display the result
        if st.button("Execute Query"):
            try:
                # Execute the custom query
                result = execute_sql_query(DB_PATH, custom_query)
                
                # Drop index column from result
                result = result.reset_index(drop=True)
                
                # Show the query result (this will overwrite the initial table)
                st.write(result)

            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
# Run the app
if __name__ == '__main__':
    main()